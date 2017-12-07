#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from __future__ import division

'''
# @file used_files.py
# @brief Extract file access data after build, modify CDT project configuration
# (.cproject) accordingly
# @copyright Copyright (C) 2016, Elphel.inc.
# @param <b>License</b>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.

@author:     Andrey Filippov
@copyright:  2015 Elphel, Inc.
@license:    GPLv3.0+
@contact:    andrey@elphel.coml
@deffield    updated: Updated
'''
__author__ = "Andrey Filippov"
__copyright__ = "Copyright 2015, Elphel, Inc."
__license__ = "GPL"
__version__ = "3.0+"
__maintainer__ = "Andrey Filippov"
__email__ = "andrey@elphel.com"
__status__ = "Development"

import os
import sys
import time
import subprocess
import datetime
import xml.etree.ElementTree
MAIN_SRC = 'src' # main source subdirectory path relative to project directory. SHould not be './' !
#    print (" cwd=",os.getcwd())
def get_bitbake_target(project_root):
    cproject_path = os.path.join(project_root,".cproject")
    try:
        return xml.etree.ElementTree.parse(cproject_path).getroot().find(
        'storageModule/cconfiguration/storageModule/configuration/folderInfo/toolChain/builder').get('arguments').split()[0]
    except:
        return None

def file_tree(flist): # Each file in list is a file, no directories
    ftree={}
    for p in flist:
        node = ftree
        seg_list=p.split(os.sep)
        last_i=len(seg_list)-1
        for i,segm in enumerate(seg_list):
            if not segm in node:
                if i == last_i:
                    node[segm] = None
                else:
                    node[segm] = {}
            node=node[segm]

    return ftree

def exclude_list(ftree, flist):
    mark = "*" # no file/dir name can be "*"
    def list_tree_recursive(root):
        rslt = []
        if not mark in root:
            return [[""]] # convert to trailing "/" for directories
        for n in root:
            if not n == mark:
                if root[n] is None:
                    rslt.append([n])
                else:

                    for l in list_tree_recursive(root[n]):
                        rslt.append([n]+l)
        return rslt

    ftree[mark]=None # mark top level dir
    for p in flist:
        node = ftree
        for segm in p.split(os.sep)[:-1]:
            node=node[segm]
            node[mark]=None # [mark] means used in flist
        del node[p.split(os.sep)[-1]]
    #print (ftree)
#    for k in ftree:
#       print(k)
    #Now prune unused directories
    #prune_recursive(ftree) # (assuming root is used)
    # now create list
    files_list_list = list_tree_recursive(ftree)
#    print (files_list_list)
    #converrt to file paths
    pl = []
    for l in files_list_list:
        pl.append(os.path.join(*(l[1:])))
    pl = sorted (pl)
    return pl

def get_sourceEntries(xml_root, root_dir):
#    main_src = 'src' # main source folder
    for sm in xml_root.iter('storageModule'):
        attr = sm.attrib
        try:
            if sm.attrib['moduleId'] !=  'cdtBuildSystem':
                continue
        except:
            continue
        for se in sm.iter('sourceEntries'):
            for en in se:
                if en.tag == 'entry':
                    attr = en.attrib
                    try:
                        if (attr['kind'] ==  'sourcePath') and (attr['name'] ==  root_dir):
                            se.remove (en)
                            print ("Removed existing entry, name= ",attr['name'])
                            return se
                    except:
                        print ("error matching attributes for ",en.tag)
                        pass
        #look for MAIN_SRC entry
        for se in sm.iter('sourceEntries'):
            for en in se:
                if en.tag == 'entry':
                    attr = en.attrib
                    try:
                        if (attr['kind'] ==  'sourcePath') and (attr['name'] ==  MAIN_SRC):
                            print ("Found existing entry for main source folder, name= ",attr['name'])
                            return se
                    except:
                        print ("error matching attributes for ",en.tag)
                        pass

        #create new sourceEntries
        print ("Creating new sourceEntries element")
        try:
            se = xml.etree.ElementTree.SubElement(sm.find('configuration'), 'sourceEntries')
            #first entry - src folder
            xml.etree.ElementTree.SubElement(se, 'entry', {"flags":"VALUE_WORKSPACE_PATH", "kind":"sourcePath", "name":MAIN_SRC})
            return se
        except:
            return None

    return None


def proc_tree(root_path, start_time, output_project_file, DEBUG): # string, float
    print("root_path=",root_path)
    print("start_time=",start_time)
    print("output_project_file=",output_project_file)
    print("DEBUG=",DEBUG)

    extensions =    [".h",".c",".cpp"]
    exclude_start = ["linux"+os.sep+"scripts"+os.sep,"linux"+os.sep+"source"+os.sep+"scripts"+os.sep]
    delta_t = 3 # seconds
#    try:
#        start_time = float(sys.argv[2])
#    except:
#        start_time = 0.0

    touch_files= start_time < 0.0
    print ("root_path = %s"%(root_path))
#    root_path = "/home/eyesis/git/poky/linux-elphel/linux/"
    lstFiles = []
    # Append  files to a list
    for path, _, files in os.walk(root_path, followlinks = True):
        for f in files:
            for ext in extensions:
                if f.endswith(ext):
                    lstFiles.append(os.path.join(path, f))
                    break

    all_tree= file_tree(sorted(lstFiles))
    include_lst=[]
    lst_a = []
    latest_at=0
    for p in lstFiles:
        if touch_files:
            if  os.path.islink(p):
                try:
                    os.utime(os.path.realpath(p), None)
                except:
                    print("missing linked file: %s"%(os.path.realpath(p)))
            else:
                os.utime(p, None)
        else:
#           at = time.ctime(os.stat(p).st_atime)
            try:
                at = os.stat(p).st_atime
                l = None
            except:
                at = 0
            if  os.path.islink(p):
                try:
                    l = os.path.realpath(p)
                    at = os.stat(l).st_atime
                except:
                    at = 0 # missing file
            latest_at = max((latest_at,at))
            if at > (start_time + delta_t):
                #Scripts/lexers result in problems
                exclude=False
                for exStr in exclude_start:
                    if p.startswith(exStr):
                        break
                else:
                  lst_a.append([p,at,l])
                  include_lst.append(p)

    if touch_files:
        print (len(lstFiles), "last time = ", time.time())
        return time.time()
    excluding = exclude_list(all_tree, include_lst)
#    print (all_tree)
#    print (sorted(include_lst))
#    print ("|".join(excluding))
#os.sep.join(s1.split(os.sep)[1:])
    including=[]
    #get rid of top directory in include paths
    for p in include_lst:
        including.append(os.sep.join(p.split(os.sep)[1:]))
    if DEBUG:
        with open("all_sources.lst","w" ) as f:
            for p in sorted(lstFiles):
                try:
                    at = os.stat(p).st_atime
                except:
                    at = 0
                lnk=""
                if  os.path.islink(p):
                    try:
                        at = os.stat(os.path.realpath(p)).st_atime
                    except:
                        at = 0
                    lnk = os.path.realpath(p)
                print (p,at,lnk, file=f)
        with open("excluding.lst","w" ) as f:
            for p in excluding:
                print (p, file=f)
        with open("including.lst","w" ) as f:
            for p in including:
                print (p, file=f)
#    include_tree= file_tree(sorted(include_lst))
#    print(include_tree)
    try:
        root_dir=include_lst[0].split(os.sep)[0] #may fail if list is empty
        print ("root_dir=",root_dir)
    except:
        print ("No files used from ",root_path)
        root_dir=root_path

    root= xml.etree.ElementTree.parse(".cproject").getroot()

    if len(include_lst):
        se = get_sourceEntries(root, root_dir)
        if se is None:
            print ("No sourceEntries exist and could not create one")
            return -1
        #add other header files in header directory, excluding...
    #    if len(excluding) < len(including):
        xml.etree.ElementTree.SubElement(se,
                                            'entry',
                                            {"flags":"VALUE_WORKSPACE_PATH", "kind":"sourcePath", "name":root_dir, "excluding":"|".join(excluding)})

    #   else:
    #               xml.etree.ElementTree.SubElement(se,
    #                                         'entry',
    #                                          {"flags":"VALUE_WORKSPACE_PATH", "kind":"sourcePath", "name":root_dir, "including":"|".join(including)})


    for child in root.iter('sourceEntries'):
        for gchild in child:
            print("tag=",gchild.tag," name=",gchild.attrib['name']," kind=",gchild.attrib['kind'])
    oneliner= xml.etree.ElementTree.tostring(root)
    #overwrites original .cproject, may change to somethong different
    with open(output_project_file, "wr") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?fileVersion 4.0.0?>""")
        f.write(oneliner)

    print (len(lstFiles), len(lst_a), "last access time = ",latest_at)
    return latest_at

def main():
    DEBUG = False
    output_project_file=".cproject" #".cproject_new" Overwrite or save to a new file
    argv = sys.argv
    top_h_dir='sysroots'
    if len(argv) < 2:
        print ("""
   This program creates a list of the source files (such as C headers) used to build the project
for Eclipse CDT plugin. It only needs to be run for the new projects, the existing ones already
have .cproject file distributed in each subproject repository (in 'eclipse_project_setup' sub-
directory of the root sub-project directory). This sub-directory content is copyied to the sub-
project root by setup.py when it is first run. You may delete .project file (while Eclipse is closed)
and re-run setup.py (in elphel393 directory) restore default project settings if they get corrupted.

   The program does not rely on exact duplicating of the environment used by bitbake, instead it
"spies" on the bitbake by noticing which files it accesses during build (using file modification and
access timestamps) and creates list of exclusions. As the access time is recorded only after the first
access after modification, the program first unpacks/touches the sources.

The extra_source directory is the specified in the command line directory (in addition to hard-coded
'src') with sub-tree of the source files (headers) to be filtered.

Here is the full sequence (target is the project name extracted from .cproject):
1. bitbake target-c cleansstate
2. bitbake target-c unpack -f
3. bitbake target-c configure -f
4. Scan all files under extra_source directory, find last modification stamp
5. bitbake target-c compile -f
6. bitbake target-c install -f # in the case of Linux kernel in triggers compilation of the kernel
   modules
7. Scan source files, create list of the used files and then list of excluded files (Eclipse CDT allows
to specify directory and exclusion filter)
8. Add (or replace) the record in .cproject file that specifies source directory and the filter

You need to run indexing  (right-click on the project in the Navigator panel -> Index -> rebuild
when the workspace is opened with the modified .cproject file.

Do not run this program when Eclipse IDE is opened that includes the current project!

The program should be launched from the project root directory, e.g. for applications:
    ./scripts/used_files.py sysroots

Program can either overwrite the current .cproject configuration file or create a new modified version
if specified in teh command line argument. In that case program runs in debug mode and generates lists
of files in the project root directory:
    all_sources.lst - all scanned source file with last access timestamps
    including.lst - list of the files (relative to specified extra_source directory) used by bitbake
    excluding.lst - list of the unused files (they will appear crossed in the Project Navigator)

USAGE:
   %s extra_source [path-to-modified-cproject]

   First (mandatory) argument of this program (extra_source) is the relative path additional source/header
   files. For Linux kernel development it is 'linux', for php extension - 'php, for applications - 'sysroots'
   (symlink to header files)

   Second (optional) argument (path-to-modified-cproject) is the relative to project root file to write
   modified .cproject content. If specified it forces program to run in debug mode and generate 3 file lists.
"""%(argv[0],))
        return 0
# Check that there is MAIN_SRC ('src') subdirectory in the project directory
    if not os.path.isdir(MAIN_SRC):
        print("\n*** Project source files should be in subdirectory '%s' for this program to run. ***\n"%(MAIN_SRC,))
        return 1
    top_h_dir = argv[1]
    if len(argv) > 2:
        output_project_file = argv[2] # Save result .cproject to a new file
        DEBUG = True

    print (" cwd=",os.getcwd())
    bitbake_target = get_bitbake_target(os.getcwd())
    print ("bitbake target=",bitbake_target)

    if not bitbake_target:
        print ("Failed to find bitbake target from .cproject file (it has to be set up in project->properties->C/C++ Build command")
        print ("For example: ${workspace_loc:/linux-elphel/scripts/run_bitbake.sh} linux-xlnx")
        return 1
    bitbake = './scripts/run_bitbake.sh'
    cmnd = bitbake+ ' '+bitbake_target+' -c cleansstate'
#   subprocess.call("ls -all", shell = True)
    return_code = subprocess.call(cmnd, shell = True)
    print ('Command: %s returned %d'%(cmnd,return_code))
    cmnd = bitbake+ ' '+bitbake_target+' -c unpack -f'
    return_code = subprocess.call(cmnd, shell = True)
    print ('Command: %s returned %d'%(cmnd,return_code))
    cmnd = bitbake+ ' '+bitbake_target+' -c configure -f'
    return_code = subprocess.call(cmnd, shell = True)
    print ('Command: %s returned %d'%(cmnd,return_code))

    last_mod = proc_tree(top_h_dir, -1.0, output_project_file,  DEBUG);
    print ('last_mod=',last_mod)
    print("waiting 5 seconds")
    time.sleep(5)
    print("waiting over")
    cmnd = bitbake+ ' '+bitbake_target+' -c compile -f'
    return_code = subprocess.call(cmnd, shell = True)
    print ('Command: %s returned %d'%(cmnd,return_code))
    cmnd = bitbake+ ' '+bitbake_target+' -c install -f'
    return_code = subprocess.call(cmnd, shell = True)
    print ('Command: %s returned %d'%(cmnd,return_code))

    latest_at = proc_tree(top_h_dir, last_mod+3, output_project_file, DEBUG);
    print ('latest_at=',latest_at)

    return 0

if __name__ == "__main__":
    sys.exit(main())