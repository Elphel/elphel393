# elphel393
installation script for fetching and setting up building environment for elphel393 camera images

### Get environment
#### Stable
```sh
$ source setup.sh
```
#### Latest
```sh
$ source setup.sh dev
```

* Will switch directory to *poky/build*

### Build targets all at once
```sh
$ bitbake u-boot device-tree linux-xlnx core-image-elphel393
```
* poky might require installing some packages, please check with the [Yocto Poky Manual][1] 
* the results are in *poky/build/tmp/deploy/images/elphel393/*
* for more info, read [here][2]
* 
[1]: http://www.yoctoproject.org/docs/2.0/mega-manual/mega-manual.html
[2]: http://wiki.elphel.com/index.php?title=Poky_2.0_manual
