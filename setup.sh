#!/bin/bash
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

#X393_SATA
E393_SATA_FPGA1_ADDR="https://github.com/Elphel/x393_sata.git"
E393_SATA_FPGA1_ROOT="x393_sata"
E393_SATA_FPGA1_BRANCH="master"
E393_SATA_FPGA1_HASH=""

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

#META SWUPDATE
SWUADDR="https://github.com/sbabic/meta-swupdate.git"
SWUROOT="meta-swupdate"
SWUBRANCH="master"
SWUHASH="f6ab29cfac2b9c6da8881c754e2a316ea43b884d"

#META EZYNQ
EZQADDR="https://github.com/Elphel/meta-ezynq.git"
EZQROOT="meta-ezynq"
EZQBRANCH="master"
EZQHASH="00496002f513fc253f5356ee675fdcbb8b4a9962"

#META ELPHEL393
E393ADDR="https://github.com/Elphel/meta-elphel393.git"
E393ROOT="meta-elphel393"
E393BRANCH="master"
E393HASH="a93edc1f91e82e5e613fa38bd800e307c348b9ee"

# List of Elphel user space applications. The list is organized as bash array and thus have predefined structure.
# Each entry in the list consists of four elements: link to repository, application name, branch and commit hash.
# If either of the fields is not used then leave double quotes in place of this field.
APPS_ARRAY=(
#imgsrv
"https://github.com/Elphel/elphel-apps-imgsrv.git"
"elphel-apps-imgsrv"
"master"
""
#php extension
"https://github.com/Elphel/elphel-apps-php-extension.git"
"elphel-apps-php-extension"
"master"
""
#camogm
"https://github.com/Elphel/elphel-apps-camogm.git"
"elphel-apps-camogm"
"master"
""
#udev rules
"https://github.com/Elphel/elphel-udev-rules.git"
"elphel-udev-rules"
"master"
""
#web-393
"https://github.com/Elphel/elphel-web-393.git"
"elphel-web-393"
"master"
""
#apps-autocampars
"https://github.com/Elphel/elphel-apps-autocampars.git"
"elphel-apps-autocampars"
"master"
""
#apps-autoexposure
"https://github.com/Elphel/elphel-apps-autoexposure.git"
"elphel-apps-autoexposure"
"master"
""
#apps-histograms
"https://github.com/Elphel/elphel-apps-histograms.git"
"elphel-apps-histograms"
"master"
""
#web-camvc
"https://github.com/Elphel/elphel-web-camvc.git"
"elphel-web-camvc"
"master"
""
#apps-editconf
"https://github.com/Elphel/elphel-apps-editconf.git"
"elphel-apps-editconf"
"master"
""
#add new app below
)


if [ "$1" = "dev" ]; then
	E393_LINUX_HASH=""
	E393_FPGA1_HASH=""
	E393_SATA_FPGA1_HASH=""
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
		if [ ! -z $4 ]; then 
			echo "    Already cloned - checked out at $3 $4"
		else
			echo "    Already cloned - check out branch then git pull"
			cd $2
			git checkout $3
			git pull
			cd ..
		fi
	fi
}

# copy Eclipse projects settings if they are present in a special directory AND not in project directory
ECLIPSE_PROJECT_SETUP="eclipse_project_setup"
copy_eclipse_settings () {
	if [ ! -f "$1/.project" ] && [ -d "$1/$ECLIPSE_PROJECT_SETUP" ]; then
		echo "  Copying up files for Eclipse project"
		echo "  Copying $1/$ECLIPSE_PROJECT_SETUP $1"
		rsync -v -a $1/$ECLIPSE_PROJECT_SETUP/ $1/
	else
		echo "  NOT Copying up files for Eclipse project"
	fi
}

echo "Step 1: Clone kernel project
"

cloneandcheckout $E393_LINUX_ADDR $E393_LINUX_ROOT $E393_LINUX_BRANCH $E393_LINUX_HASH
if [ ! -f $E393_LINUX_ROOT/.project ]; then
	echo "  Copying up files for Eclipse project"
	echo "  Copying $E393_LINUX_ROOT/eclipse_project_setup $E393_LINUX_ROOT"
	rsync -a $E393_LINUX_ROOT/eclipse_project_setup/ $E393_LINUX_ROOT/
else
	echo "  NOT Copying up files for Eclipse project"
fi



echo "
Step 2: Clone fpga projects
"

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

cloneandcheckout $E393_SATA_FPGA1_ADDR $E393_SATA_FPGA1_ROOT $E393_SATA_FPGA1_BRANCH $E393_SATA_FPGA1_HASH

cd ..



echo "
Step 3: Clone applications and libraries projects
"

if [ ! -d $E393_ROOTFSDIR ]; then
	echo "  Creating $E393_ROOTFSDIR"
	mkdir $E393_ROOTFSDIR
else
	echo "  $E393_ROOTFSDIR exists"
fi
cd $E393_ROOTFSDIR
#Clone user space applications
for elem in $(seq 0 4 $((${#APPS_ARRAY[@]} - 1))); do
	cloneandcheckout "${APPS_ARRAY[$elem]}" "${APPS_ARRAY[$elem+1]}" "${APPS_ARRAY[$elem+2]}" "${APPS_ARRAY[$elem+3]}"
	copy_eclipse_settings "${APPS_ARRAY[$elem+1]}"
done
cd ..



echo "
Step 4: Extra meta layers
"

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
echo "  meta-swupdate:"
cloneandcheckout $SWUADDR $SWUROOT $SWUBRANCH $SWUHASH
echo "  meta-ezynq:"
cloneandcheckout $EZQADDR $EZQROOT $EZQBRANCH $EZQHASH
echo "  meta-elphel393:"
cloneandcheckout $E393ADDR $E393ROOT $E393BRANCH $E393HASH
cd ..



echo "
Step 5: Poky
"

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
echo "" >> $CONF_NOTES

CURRENT_PATH2=$(dirname $(readlink -f "$0"))
echo ""

BBLAYERS_CONF="conf/bblayers.conf"
LOCAL_CONF="conf/local.conf"

MISSING_LOCAL_CONF=0
MISSING_BBLAYERS_CONF=0

if [ ! -f build/$LOCAL_CONF ]; then
    MISSING_LOCAL_CONF=1
else
    echo "build/$LOCAL_CONF exists, updating default version: build/${LOCAL_CONF}_default"
    cp build/$LOCAL_CONF build/$LOCAL_CONF"_bkp"
    rm build/$LOCAL_CONF
fi

if [ ! -f build/$BBLAYERS_CONF ]; then
    MISSING_BBLAYERS_CONF=1
else
    echo "build/$BBLAYERS_CONF exists, updating default version: build/${BBLAYERS_CONF}_default"
    cp build/$BBLAYERS_CONF build/$BBLAYERS_CONF"_bkp"
    rm build/$BBLAYERS_CONF
fi

echo ""

echo "Running: . ./oe-init-build-env build. If config files existed they will be backed up and restored"
. ./oe-init-build-env build

echo ""

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

#distro features: systemd
#echo "DISTRO_FEATURES_append = \" systemd\"" >> $LOCAL_CONF
#echo "VIRTUAL-RUNTIME_init_manager = \"systemd\"" >> $LOCAL_CONF
#echo "DISTRO_FEATURES_BACKFILL_CONSIDERED = \"sysvinit\"" >> $LOCAL_CONF
#echo "VIRTUAL-RUNTIME_initscripts = \"\"" >> $LOCAL_CONF
# change the MACHINE
echo "MACHINE ?= \"elphel393\"" >> $LOCAL_CONF
# Elphel's MIRROR website, \n is important
echo "MIRRORS =+ \"http://.*/.*     http://mirror.elphel.com/elphel393_mirror/ \\n \"" >> $LOCAL_CONF

echo "REMOTE_USER ?= \"root\""  >> $LOCAL_CONF
echo "IDENTITY_FILE ?= \"~/.ssh/id_rsa\"" >> $LOCAL_CONF
echo "REMOTE_IP ?= \"192.168.0.9\""  >> $LOCAL_CONF

if [ $MISSING_BBLAYERS_CONF -eq 0 ]; then
    echo "restoring $BBLAYERS_CONF"
    cp $BBLAYERS_CONF $BBLAYERS_CONF"_default"
    cp $BBLAYERS_CONF"_bkp" $BBLAYERS_CONF
    echo "NOTE: If anything breaks after running setup.sh, compare your bblayers.conf and bblayers.conf_default"
fi

if [ $MISSING_LOCAL_CONF -eq 0 ]; then
    echo "restoring $LOCAL_CONF"
    cp $LOCAL_CONF $LOCAL_CONF"_default"
    cp $LOCAL_CONF"_bkp" $LOCAL_CONF
    echo "NOTE: If anything breaks after running setup.sh, compare your local.conf and local.conf_default"
fi

