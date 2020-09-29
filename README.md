# elphel393

Scripts for setting up development environment to build firmware for Elphel393 camera systems.

Prebuilt firmware: [community.elphel.com/files/393/](http://community.elphel.com/files/393/).

## Requirements

### for Kubuntu 20.04 
* poky might require installing some packages, please check with the [Yocto Poky Manual](http://www.yoctoproject.org/docs/2.0/mega-manual/mega-manual.html)
* extra packages:

```sh
# in Kubuntu 20.04 this will install python2 which is used by poky[warrior]
$ sudo apt install python python-numpy python3-numpy
# below fixes missing error when compiling the kernel: missing "openssl/bio.h":
$ sudo apt install libssl-dev
```

### for Kubuntu 16.04/18.04
* same as for Kubuntu 20.04
* run setup.py then roll back [meta-elphel393](https://git.elphel.com/Elphel/meta-elphel393) to [6e0687d745e8962ec979e59ed600203c97d92cff](https://git.elphel.com/Elphel/meta-elphel393/commit/6e0687d745e8962ec979e59ed600203c97d92cff)

## Clone this repo ('warrior' branch recommended)

```sh
$ git clone -b warrior https://git.elphel.com/Elphel/elphel393.git
```

## Setup
```sh
$ ./setup.py
```

## Build
```sh
$ cd poky
$ . ./oe-init-build-env
$ bitbake u-boot device-tree linux-xlnx core-image-elphel393
```

* the results are in *bootable-images/*
* for more details, read [**this guide**][1] at [https://wiki.elphel.com][1]

[1]: http://wiki.elphel.com/index.php?title=Poky_2.0_manual

## Update and refresh environment
```sh
$ ./setup.py
```
## Rebuild targets
```sh
$ cd poky
$ . ./oe-init-build-env
$ (if changes in the kernel) bitbake linux-xlnx -c link -f; bitbake linux-xlnx
$ (if changes in the rootfs and the kernel) bitbake core-image-elphel393
```

## More info

[**Development for 10393**](https://wiki.elphel.com/wiki/Development_for_10393)

## Support

support-list@support.elphel.com
