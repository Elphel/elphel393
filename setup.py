#!/usr/bin/env python

# Clones and sets up and updates everything, also creates local.conf

__author__ = "Elphel"
__copyright__ = "Copyright 2016, Elphel, Inc."
__license__ = "GPL"
__version__ = "3.0+"
__maintainer__ = "Oleg K Dzhimiev"
__email__ = "oleg@elphel.com"
__status__ = "Development"

import subprocess
import os
import sys

Projects = {
    'meta'  : {
        'meta-openembedded':[
            'git://git.openembedded.org/meta-openembedded',
            'master','73854a05565b30a5ca146ac53959c679b27815aa',
            ],
        'meta-xilinx':[
            'https://github.com/Xilinx/meta-xilinx.git',
            'master','cc146d6c170f100eb2f445047969893faa7a6a55'
            ],
        'meta-swupdate':[
            'https://github.com/sbabic/meta-swupdate.git',
            'master','f6ab29cfac2b9c6da8881c754e2a316ea43b884d'
            ],
        'meta-ezynq':[
            'https://github.com/Elphel/meta-ezynq.git',
            'master',''
            #'master','00496002f513fc253f5356ee675fdcbb8b4a9962'
            ],
        'meta-elphel393':[
            'https://github.com/Elphel/meta-elphel393.git',
            'master',''
            #'master','a93edc1f91e82e5e613fa38bd800e307c348b9ee'
            ],
    },
    'poky':[
        'git://git.yoctoproject.org/poky.git',
        'master','3d2c0f5902cacf9d8544bf263b51ef0dd1a7218c'
        ],
    'fpga-elphel'  : {
        'x393'     :[
            'https://github.com/Elphel/x393.git',
            'master',''
            #'master','edcdce9550c20726618210149bc1cb4549fd00be'
            ],
        'x393_sata':[
            'https://github.com/Elphel/x393_sata.git',
            'master',''
            ],
        'x359'     :[
            'https://github.com/Elphel/x359.git',
            'master',''
            ],
        },
    'linux-elphel' :[
        'https://github.com/Elphel/linux-elphel.git',
        'master',''
        #'master','cc50d7fa07140e680b09a8add617e62b4ba35aa0'
        ],
    'rootfs-elphel': {
        'elphel-apps-imgsrv':[
            'https://github.com/Elphel/elphel-apps-imgsrv.git',
            'master',''
            ],
        'elphel-apps-php-extension':[
            'https://github.com/Elphel/elphel-apps-php-extension.git',
            'master',''
            ],
        'elphel-apps-camogm':[
            'https://github.com/Elphel/elphel-apps-camogm.git',
            'master',''
            ],
        'elphel-udev-rules':[
            'https://github.com/Elphel/elphel-udev-rules.git',
            'master',''
            ],
        'elphel-web-393':[
            'https://github.com/Elphel/elphel-web-393.git',
            'master',''
            ],
        'elphel-apps-autocampars':[
            'https://github.com/Elphel/elphel-apps-autocampars.git',
            'master',''
            ],
        'elphel-apps-autoexposure':[
            'https://github.com/Elphel/elphel-apps-autoexposure.git',
            'master',''
            ],
        'elphel-apps-histograms':[
            'https://github.com/Elphel/elphel-apps-histograms.git',
            'master',''
            ],
        'elphel-web-camvc':[
            'https://github.com/Elphel/elphel-web-camvc.git',
            'master',''
            ],
        'elphel-apps-editconf':[
            'https://github.com/Elphel/elphel-apps-editconf.git',
            'master',''
            ],
        'elphel-init':[
            'https://github.com/Elphel/elphel-init.git',
            'master',''
            ],
        'elphel-web-hwmon':[
            'https://github.com/Elphel/elphel-web-hwmon.git',
            'master',''
            ],
        'elphel-apps-tempmon':[
            'https://github.com/Elphel/elphel-apps-tempmon.git',
            'master',''
            ],
        'elphel-apps-gps':[
            'https://github.com/Elphel/elphel-apps-gps.git',
            'master',''
            ],
        },
    'tools' : {
        'elphel-tools-update':[
            'https://github.com/Elphel/elphel-tools-update.git',
            'master',''
            ]
        },
}
        
#http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[38;5;214m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BOLDWHITE = '\033[1;37m'
    UNDERLINE = '\033[4m'

def shout(cmd):
    subprocess.call(cmd,shell=True)

def cloneandcheckout(name,item):
    print("Clone and checkout: "+name)
    if not os.path.isdir(name):
        print(bcolors.WARNING+"    Cloning into "+name+", branch="+item[1]+", hash="+item[2]+bcolors.ENDC)
        shout("git clone -b "+item[1]+" "+item[0]+" "+name)
        cwd = os.getcwd()
        os.chdir(cwd+"/"+name)
        shout("git checkout "+item[2])
        os.chdir(cwd)
    else:
        #check for https or git
        
        cwd = os.getcwd()
        os.chdir(cwd+"/"+name)
        read_remote = subprocess.check_output("git remote -v",shell=True)
        if read_remote.find(item[0])==-1:
            print(bcolors.WARNING+"Changing git remote to "+item[0]+bcolors.ENDC)
            shout("git remote set-url origin "+item[0])
        os.chdir(cwd)
        
        if item[2]!="":
            print("    Already cloned - checked out at "+item[1]+" "+item[2])
        else:
            print("    Already cloned - check out branch then git pull")
            cwd = os.getcwd()
            os.chdir(cwd+"/"+name)
            cmd = "git checkout "+item[1]+" | grep --color -E '^|^M\s(.*)$'"
            shout(cmd)
            shout("git pull")
            os.chdir(cwd)

def copy_eclipse_settings(name):
    EPS = "eclipse_project_setup"
    if (not os.path.isfile(name+"/.project")) and (os.path.isdir(name+"/"+EPS)):
        print("  Copying up files for Eclipse project")
        print(bcolors.WARNING+"  Copying "+name+"/"+EPS+" to "+name+"/"+bcolors.ENDC)
        shout("rsync -v -a "+name+"/"+EPS+" "+name+"/")
    else:
        print("Not copying up files for Eclipse project: .project is already there")

def read_local_conf(conf_file,pattern):
    ret = []
    if os.path.isfile(conf_file):
        with open(conf_file,"r") as f:
            lines = f.readlines()
            for line in lines:
                test = line.find(pattern)
                if test!=-1:
                    pars = line.split("=")[1].strip().strip("\"").split(":")
                    ret.append(pars)
    return ret

def read_local_conf_dev(conf_file,pattern):
    ret = "0"
    if os.path.isfile(conf_file):
        with open(conf_file,"r") as f:
            lines = f.readlines()
            for line in lines:
                test = line.find(pattern)
                if test!=-1:
                    ret = line.split("=")[1].strip().strip("\"")
    return ret

def update_branch(names_from_conf,name_from_list,pars,git_proto):
    if (git_proto=="1"):
        tmp = "https://github.com/Elphel"
        if pars[0].find(tmp)!=-1:
            pars[0] = "git@github.com:Elphel"+pars[0][len(tmp):]
    else:
        tmp = "git@github.com:Elphel"
        if pars[0].find(tmp)!=-1:
            pars[0] = "https://github.com/Elphel"+pars[0][len(tmp):]
            
    for p in names_from_conf:
        if name_from_list in p:
            pars[1] = p[1]
    return pars

#main
project_branches = read_local_conf("poky/build/conf/local.conf","ELPHEL393_branches")
git_proto = read_local_conf_dev("poky/build/conf/local.conf","ELPHEL393_DEV")
i=0
for p,v in Projects.items():
    i = i + 1
    print bcolors.BOLDWHITE+"Step "+str(i)+": "+p+bcolors.ENDC
    
    if isinstance(v,dict):
        #create dir
        if not os.path.isdir(p):
            print("  Creating "+p)
            os.mkdir(p)
        else:
            print("  "+p+" exists")
        
        cwd = os.getcwd()
        os.chdir(cwd+"/"+p)
        
        for k,l in v.items():
            print("\n"+bcolors.BOLDWHITE+"*"+bcolors.ENDC+" "+k)
            cloneandcheckout(k,update_branch(project_branches,k,l,git_proto))
            copy_eclipse_settings(k)
            
            #special case for x393 fpga project
            if k=="x393":
                if os.path.isfile(k+"/py393/generate_c.sh"):
                    subcwd = os.getcwd()
                    os.chdir(subcwd+"/"+k+"/py393")
                    shout("./generate_c.sh")
                    os.chdir(subcwd)
                if os.path.isdir(k+"/py393/generated"):
                    if os.path.isdir(cwd+"/linux-elphel/src/drivers/elphel"):
                        shout("rsync -a "+k+"/py393/generated/ "+cwd+"/linux-elphel/src/drivers/elphel")
        os.chdir(cwd)
    
    elif isinstance(v,list):
        cloneandcheckout(p,update_branch(project_branches,p,v,git_proto))
        copy_eclipse_settings(p)
        
    else:
        print("Error?")


# do the local.conf
path = os.getcwd()
os.chdir(path+"/poky")

conf_notes = "meta-yocto/conf/conf-notes.txt"

if os.path.isfile(conf_notes):
    os.remove(conf_notes)
    with open(conf_notes,'w') as f:
        f.write("""\
Common targets for \"elphel393\" camera series are:
    u-boot
    device-tree
    linux-xlnx
    core-image-elphel393
""")

bblayers_conf = "build/conf/bblayers.conf"
local_conf = "build/conf/local.conf"

missing_local_conf = 0
missing_bblayers_conf = 0

if not os.path.isfile(local_conf):
    missing_local_conf = 1
else:
    print("\n"+local_conf+" exists, updating the default version: "+local_conf+"_default")
    shout("cp "+local_conf+" "+local_conf+"_bkp")
    os.remove(local_conf)

if not os.path.isfile(bblayers_conf):
    missing_bblayers_conf = 1
else:
    print(bblayers_conf+" exists, updating the default version: "+bblayers_conf+"_default")
    shout("cp "+bblayers_conf+" "+bblayers_conf+"_bkp")
    os.remove(bblayers_conf)

print("Running: . ./oe-init-build-env build. If config files existed they will be backed up and restored")

shout(". ./oe-init-build-env build")

with open(bblayers_conf,"a") as f:
    f.write("""\
BBLAYERS = " \\
  {0}/poky/meta \\
  {0}/poky/meta-yocto \\
  {0}/poky/meta-yocto-bsp \\
  {0}/meta/meta-ezynq \\
  {0}/meta/meta-elphel393 \\
  {0}/meta/meta-xilinx \\
  {0}/meta/meta-openembedded/meta-oe \\
  {0}/meta/meta-openembedded/meta-python \\
  {0}/meta/meta-openembedded/meta-networking \\
  {0}/meta/meta-openembedded/meta-webserver \\
  "
""".format(path))
    
with open(local_conf,"a") as f:
    f.write("""\

MACHINE ?= "elphel393"
MIRRORS =+ "http://.*/.*     http://mirror.elphel.com/elphel393_mirror/ \\n "

# To change a project's branch from the setup.py list to something other than 'master'
# add the following line (a separate line for each project):
# ELPHEL393_branches += "projectname:branchname"
# Example:
# ELPHEL393_branches += "elphel-apps-camogm:framepars"
# ELPHEL393_branches += "linux-elphel:framepars"

# By default the projects' remotes are set to https.
# To switch to git:// (commit changes to github w/o a password)
# uncomment the following line
# 1 - for git://   - access using a key
# 0 (or commented) - for https:// - access using a password
# ELPHEL393_DEV = "1"

REMOTE_USER ?= "root"
IDENTITY_FILE ?= "~/.ssh/id_rsa"

REMOTE_IP ?= "192.168.0.9"

INITSTRING ?= "init_elphel393.py \\"{\\
    \\\\"usb_hub\\\\"  :1,\\
    \\\\"ip\\\\"       :1,\\
    \\\\"mcntrl\\\\"   :1,\\
    \\\\"imgsrv\\\\"   :1,\\
    \\\\"port1\\\\"    :1,\\
    \\\\"port2\\\\"    :1,\\
    \\\\"port3\\\\"    :1,\\
    \\\\"port4\\\\"    :1,\\
    \\\\"framepars\\\\":1,\\
    \\\\"autoexp_daemon\\\\"  :1,\\
    \\\\"autoexp\\\\"  :1,\\
    \\\\"autowb\\\\"   :1,\\
    \\\\"sata\\\\"     :1,\\
    \\\\"gps\\\\"      :1,\\
    \\\\"eyesis\\\\"   :0 \\
}\\""
MACHINE_DEVICETREE = "elphel393_4_mt9p006.dts"
""")

if missing_bblayers_conf==0:
    print("restoring "+bblayers_conf)
    shout("cp "+bblayers_conf+" "+bblayers_conf+"_default")
    shout("cp "+bblayers_conf+"_bkp "+bblayers_conf)
    print("NOTE: If anything breaks after running setup.sh, compare your bblayers.conf and bblayers.conf_default")
    
if missing_local_conf==0:
    print("restoring "+local_conf)
    shout("cp "+local_conf+" "+local_conf+"_default")
    shout("cp "+local_conf+"_bkp "+local_conf)
    print("NOTE: If anything breaks after running setup.sh, compare your local.conf and local.conf_default")
