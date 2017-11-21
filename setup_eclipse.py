#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from __future__ import division

'''
# Copyright (C) 2017, Elphel.inc.
# Setup eclipse workspace for multiple projects of elphel393
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
import subprocess
import datetime
import xml.etree.ElementTree
def main():
    workspace = '../workspace-elphel393'
    project_paths = "./setup_eclipse_paths.xml"
    continue_setup = False # True # disable later
    argv = sys.argv
    print (argv)
    if (len(argv) < 2):
        print ("""
   This program creates new Eclipse workspace for all elphel393 subprojects. Eclipse installation
should have CDT and EGit plugins installed.
USAGE:
   %s eclipse-home [[path-to-workspace] project-paths]
   First (mandatory) argument of this program (eclipse-home) is the full path to Eclipse installation
   (directory that has eclipse executable and eclipse.ini files).
   Second (optional) argument (path-to-workspace) is the path to workspace. If not specified,
   then ../workspace_elphel393 will be used.
   Third (optional) argument (project-paths) is the path to list of project paths. If not specified,
   then "./setup_eclipse_paths.

The program will not overwrite or modify any existing workspace.        
"""%(argv[0],))
        return 0
    eclipse_home = argv[1]
        
    if (len(argv) > 3):
        project_paths = argv[3]
    project_paths = os.path.abspath(project_paths)
    proj_paths_root = xml.etree.ElementTree.parse(project_paths).getroot()#.find('name').text
    subprojects = []
    for child in proj_paths_root:
        subprojects.append(child.text)
    print('subprojects=',subprojects)    

    if (len(argv) > 2):
        workspace = argv[2]
        
    workspace = os.path.abspath(workspace)
    need_import = True    
    if os.path.exists(workspace):
        if continue_setup:
            print ("Workspace %s already exists, will continue to set up git"%(workspace,))
            need_import = False            
        else:    
            print ("Workspace %s already exists, this  program can not modify/overwrite existing workspaces"%(workspace,))
            return 1
    apath=os.path.dirname(os.path.abspath(argv[0]))
    print ("scriptdir=",apath," cwd=",os.getcwd())
    #create eclipse import command
    eclipse_import = os.path.join(eclipse_home,"eclipse" +
                      " -nosplash" + 
                      " -data "+ workspace +
                      " -application org.eclipse.cdt.managedbuilder.core.headlessbuild")
#    print ("subprojects=",subprojects)
    for project in subprojects:
        eclipse_import += " -import " + os.path.join(apath,project)
        
    eclipse_import += " -no-indexer"  # disableto create indexes (slow)        
          
    print ("eclipse_import = ",eclipse_import)
    return_code = -1
    if need_import:
        return_code = subprocess.call(eclipse_import, shell = True)
    print ("Eclipse import returned ",return_code)
    if return_code > 0:
        print ("Can not continuie on error")
        return 1
    #creating workspace/.metadata/.plugins/org.eclipse.core_runtime/.settings/org.eclipse.egit.core.prefs
    egit_prefs_path = os.path.join(workspace,".metadata",".plugins","org.eclipse.core.runtime",".settings","org.eclipse.egit.core.prefs")
    egit_prefs="GitRepositoriesView.GitDirectories="
    for project in subprojects:
        egit_prefs += os.path.join(apath,project,".git") + "\\:"
    egit_prefs += "\n"
    egit_prefs += "GitRepositoriesView.GitDirectories.relative=" 
    for project in subprojects:
        egit_prefs += os.path.join(apath,project,".git") + "\\:"
    egit_prefs += "\n"
    egit_prefs += "RepositorySearchDialogSearchPath=" + apath + "\n"
    egit_prefs += "eclipse.preferences.version=1\n"
    print ("Creating file ",egit_prefs_path)
    print (egit_prefs)
    with open(egit_prefs_path, 'w') as f:
        print (egit_prefs,file = f)
        
#Create per-project files (and last directory):
    
    GitProjectData= "#GitProjectData\n#"+datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")+"\n.gitdir=.git\n"
    print ("GitProjectData=",GitProjectData)
    #strings to be encoded in properties.index files (now, with fresh workspace never opened - all the same)
    bin_strings = ['org.eclipse.team.core',
                   'repository',
                   'org.eclipse.egit.core.GitProvider']
    for project in subprojects:
        #read project names
        dot_proj_path=os.path.join(apath,project,".project")
        proj_name = xml.etree.ElementTree.parse(dot_proj_path).getroot().find('name').text
        print(proj_name, dot_proj_path)
        workspace_proj_path = os.path.join(workspace,
                                           '.metadata',
                                           '.plugins',
                                           'org.eclipse.core.resources',
                                           '.projects',
                                           proj_name)# ,        org.eclipse.egit.core/
        egit_core_dir= os.path.join(workspace_proj_path, 'org.eclipse.egit.core')
        if not os.path.exists(egit_core_dir):
            os.makedirs(egit_core_dir)
            print ('created new directory ',egit_core_dir)
        else:
            print ('directory ',egit_core_dir,' already existed')
        GitProjectDataPath=os.path.join(egit_core_dir, 'GitProjectData.properties')
        # Write GitProjectData.properties contents
        with open(GitProjectDataPath, 'w') as f:
            print (GitProjectData,file = f)
        # Create .indexes subdirectory in project subdirectory
        indexes_dir= os.path.join(workspace_proj_path, '.indexes')
        if not os.path.exists(indexes_dir):
            os.makedirs(indexes_dir)
            print ('created new directory ',indexes_dir)
        else:
            print ('directory ',indexes_dir,' already existed')
        properties_index=    os.path.join(indexes_dir, 'properties.index')
        data = [1,0,0,0,
                1,0,0,0,
                1, # single pair entry
                2, # 3 strings to follow
                ]
        #now create binary file
        for bin_str in bin_strings:
#            print (len(bin_str), bin_str)
            data.append(0) #these strings are never longer than 255
            data.append(len(bin_str))
            for l in bin_str:
                data.append(ord(l))
        ba=bytearray(data)
        with open(properties_index, 'w') as f:
            f.write(ba)
         
if __name__ == "__main__":
    sys.exit(main())    