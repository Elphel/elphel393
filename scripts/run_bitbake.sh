#!/bin/bash
#ls -all
args="$@"
arg0=$0 
#echo "arg0=" $arg0
#echo "args=" $args

while (( "$#" )); do
  shift
done
#DIR0="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR=$(dirname $(dirname $(dirname $(realpath $(dirname $(dirname $arg0))/sysroots))))

echo "DIR=" $DIR
echo "Launching bitbake $args"
#cd $DIR0/../../poky
cd $DIR
. ./oe-init-build-env
bitbake $args  | sed -u 's@| @@'
exit 0
