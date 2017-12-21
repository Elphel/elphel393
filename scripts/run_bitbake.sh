#!/bin/bash
#ls -all
args="$@"
arg0=$0
#echo "arg0=" $arg0
#echo "args=" $args

while (( "$#" )); do
  shift
done

DIR=$(realpath $(dirname $(dirname $arg0))/sysroots)

# works for Poky Jethro - Rocko
# move up until Poky's init script is found
while ([ ! -f $DIR/oe-init-build-env ]);do
  DIR=$(dirname $DIR)
  if [ "e$DIR" = 'e/' ]; then
    break
  fi
done

echo "DIR= $DIR"
echo "Launching bitbake $args"
#cd $DIR0/../../poky
cd $DIR
. ./oe-init-build-env
bitbake $args  | sed -u 's@| @@'
exit 0
