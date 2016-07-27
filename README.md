# elphel393
Installation script for fetching and setting up building environment for elphel393 camera images,
it clones and configures several individual repositories, such as
* https://github.com/Elphel/linux-elphel
* https://github.com/Elphel/x393
* http://git.yoctoproject.org
* http://git.openembedded.org
* https://github.com/Xilinx/meta-xilinx
* https://github.com/Elphel/meta-elphel393
 
The same script pulls updates from these repositories

### Get environment
#### Stable
```sh
$ ./setup.sh
```
#### Latest
```sh
$ ./setup.sh dev
```

### Build targets
```sh
$ cd poky
$ . ./oe-init-build-env
$ bitbake u-boot device-tree linux-xlnx core-image-elphel393
```
* poky might require installing some packages, please check with the [Yocto Poky Manual][1] 
* the results are in *poky/build/tmp/deploy/images/elphel393/*
* for more info, read [here][2]

[1]: http://www.yoctoproject.org/docs/2.0/mega-manual/mega-manual.html
[2]: http://wiki.elphel.com/index.php?title=Poky_2.0_manual
