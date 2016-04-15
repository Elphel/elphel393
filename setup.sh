#!/bin/sh
# Download and setup everything

E393_METADIR="meta"
E393_FPGADIR="fpga-elphel"
E393_ROOTFSDIR="rootfs-elphel"

#LINUX ELPHEL
E393_LINUX_ADDR="https://github.com/Elphel/linux-elphel.git"
E393_LINUX_ROOT="linux-elphel"
E393_LINUX_BRANCH="master"
E393_LINUX_HASH="cc50d7fa07140e680b09a8add617e62b4ba35aa0"

#X393
E393_FPGA1_ADDR="https://github.com/Elphel/x393.git"
E393_FPGA1_ROOT="x393"
E393_FPGA1_BRANCH="master"
E393_FPGA1_HASH="edcdce9550c20726618210149bc1cb4549fd00be"

#POKY
POKYADDR="git://git.yoctoproject.org/poky.git"
POKYROOT="poky"
POKYBRANCH="master"
POKYHASH="3d2c0f5902cacf9d8544bf263b51ef0dd1a7218c"

#META OPENEMBEDDED
MOEADDR="git://git.openembedded.org/meta-openembedded"
MOEROOT="meta-openembedded"
MOEBRANCH="master"
MOEHASH="73854a05565b30a5ca146ac53959c679b27815aa"

#META XILINX
XLNXADDR="https://github.com/Xilinx/meta-xilinx.git"
XLNXROOT="meta-xilinx"
XLNXBRANCH="master"
XLNXHASH="cc146d6c170f100eb2f445047969893faa7a6a55"

#META EZYNQ
EZQADDR="https://github.com/Elphel/meta-ezynq.git"
EZQROOT="meta-ezynq"
EZQBRANCH="master"
EZQHASH="d3a055fc82fff990f9f2cdb8c09eb948133cf6f4"

#META ELPHEL393
E393ADDR="https://github.com/Elphel/meta-elphel393.git"
E393ROOT="meta-elphel393"
E393BRANCH="master"
E393HASH="a93edc1f91e82e5e613fa38bd800e307c348b9ee"

if [ $1 = "dev" ]; then
	E393_LINUX_HASH=""
	E393_FPGA1_HASH=""
	EZQHASH=""
	E393HASH=""
fi

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

cloneandcheckout () {
	if [ ! -d $2 ]; then
		echo "    Cloning into $2, branch=$3, hash=$4"
		git clone -b $3 $1 $2
		cd $2
		git checkout $4
		cd ..
	else
		echo "    Already cloned - doing nothing"
	fi
}

echo "Step 1: Clone kernel project"
cloneandcheckout $E393_LINUX_ADDR $E393_LINUX_ROOT $E393_LINUX_BRANCH $E393_LINUX_HASH
if [ ! -f $E393_LINUX_ROOT/.project ]; then
	echo "  Copying up files for Eclipse project"
	echo "  Copying $E393_LINUX_ROOT/eclipse_project_setup $E393_LINUX_ROOT"
	rsync -a $E393_LINUX_ROOT/eclipse_project_setup/ $E393_LINUX_ROOT/
else
	echo "  NOT Copying up files for Eclipse project"
fi



echo "Step 2: Clone fpga projects"
if [ ! -d $E393_FPGADIR ]; then
	echo "  Creating $E393_FPGADIR"
	mkdir $E393_FPGADIR
else
	echo "  $E393_FPGADIR exists"
fi

cd $E393_FPGADIR
cloneandcheckout $E393_FPGA1_ADDR $E393_FPGA1_ROOT $E393_FPGA1_BRANCH $E393_FPGA1_HASH
if [ -f $E393_FPGA1_ROOT/py393/generate_c.sh ]; then
	cd $E393_FPGA1_ROOT/py393
	./generate_c.sh
	cd ../..
	if [ -d $E393_FPGA1_ROOT/py393/generated ]; then
		if [ -d ../$E393_LINUX_ROOT/src/drivers/elphel ]; then
			rsync -a $E393_FPGA1_ROOT/py393/generated/ ../$E393_LINUX_ROOT/src/drivers/elphel
		fi
	fi
fi
cd ..



echo "Step 3: Clone applications and libraries projects"
if [ ! -d $E393_ROOTFSDIR ]; then
	echo "  Creating $E393_ROOTFSDIR"
	mkdir $E393_ROOTFSDIR
else
	echo "  $E393_ROOTFSDIR exists"
fi
cd $E393_ROOTFSDIR
#Clone some projects
cd ..



echo "Step 4: Extra meta layers"
if [ ! -d $E393_METADIR ]; then
	echo "  Creating $ELPHEL393_METADIR"
	mkdir $E393_METADIR
else
	echo "  $E393_METADIR exists - doing nothing"
fi
cd $E393_METADIR
echo "  meta-openembedded:"
cloneandcheckout $MOEADDR $MOEROOT $MOEBRANCH $MOEHASH
echo "  meta-xilinx:"
cloneandcheckout $XLNXADDR $XLNXROOT $XLNXBRANCH $XLNXHASH
echo "  meta-ezynq:"
cloneandcheckout $EZQADDR $EZQROOT $EZQBRANCH $EZQHASH
echo "  meta-elphel393:"
cloneandcheckout $E393ADDR $E393ROOT $E393BRANCH $E393HASH
cd ..



echo "Step 5: Poky"
cloneandcheckout $POKYADDR $POKYROOT $POKYBRANCH $POKYHASH

CURRENT_PATH1=$(dirname $(readlink -f "$0"))

cd $POKYROOT
CONF_NOTES="meta-yocto/conf/conf-notes.txt"
if [ -f $CONF_NOTES ]; then
    rm $CONF_NOTES
fi
echo "Common targets for \"elphel393\" camera series are:" >> $CONF_NOTES
echo "    u-boot" >> $CONF_NOTES
echo "    device-tree" >> $CONF_NOTES
echo "    linux-xlnx" >> $CONF_NOTES
echo "    core-image-elphel393" >> $CONF_NOTES
echo "Extra targets (somewhat useful for development) are:" >> $CONF_NOTES
echo "    update393 -c pull -f" >> $CONF_NOTES
echo "    update393 -c generate -f" >> $CONF_NOTES
echo "" >> $CONF_NOTES

CURRENT_PATH2=$(dirname $(readlink -f "$0"))
. ./oe-init-build-env build

BBLAYERS_CONF="conf/bblayers.conf"

echo "BBLAYERS = \" \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH2/meta \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH2/meta-yocto \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH2/meta-yocto-bsp \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$EZQROOT \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$E393ROOT \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$XLNXROOT \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$MOEROOT/meta-oe \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$MOEROOT/meta-python \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$MOEROOT/meta-networking \\" >> $BBLAYERS_CONF
echo "  $CURRENT_PATH1/$E393_METADIR/$MOEROOT/meta-webserver \\" >> $BBLAYERS_CONF
echo "  \"" >> $BBLAYERS_CONF

LOCAL_CONF="conf/local.conf"

# change the MACHINE
echo "MACHINE ?= \"elphel393\"" >> $LOCAL_CONF
# Elphel's MIRROR website, \n is important
echo "MIRRORS =+ \"http://.*/.*     http://mirror.elphel.com/elphel393_mirror/ \n \"" >> $LOCAL_CONF
