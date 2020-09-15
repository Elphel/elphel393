# elphel393

The project contains scripts for setting up development environment to build firmware images for Elphel393 camera systems.

**Prebuilt firmware images are available [community.elphel.com/files/393/](http://community.elphel.com/files/393/).**

### Get environment
#### Dependencies
* poky might require installing some packages, please check with the [Yocto Poky Manual](http://www.yoctoproject.org/docs/2.0/mega-manual/mega-manual.html)
* extra requirement

```sh
# in Kubuntu 20.04 this will install python2 which is used by poky[warrior]
$ sudo apt install python python-numpy
# below fixes missing error when compiling the kernel: missing "openssl/bio.h":
$ sudo apt install libssl-dev
```

#### Get sources
```sh
$ ./setup.py
```

### Build targets
```sh
$ cd poky
$ . ./oe-init-build-env
$ bitbake u-boot device-tree linux-xlnx core-image-elphel393
```

* the results are in *poky/build/tmp/deploy/images/elphel393/*
* for more details, read [**this guide**][1] at [https://wiki.elphel.com][1]

[1]: http://wiki.elphel.com/index.php?title=Poky_2.0_manual

### Update and refresh environment
```sh
$ ./setup.py
```
### Rebuild targets
```sh
$ cd poky
$ . ./oe-init-build-env
$ (if changes in the kernel) bitbake linux-xlnx -c link -f; bitbake linux-xlnx
$ (if changes in the rootfs and the kernel) bitbake core-image-elphel393
```

### More info

[**Development for 10393**](https://wiki.elphel.com/wiki/Development_for_10393)

### Support

support-list@support.elphel.com

### Note 1: Switching between GIT protocols (SSH or HTTPS)

To have access to related Elphel's projects over **SSH** clone this project using **SSH**.

For **HTTPS** clone with **HTTPS**.

To change git protocol for all Elphel's projects - change the *remote* of this project accordingly, then run *setup.py*:
```sh
$ git remote -v
$ git remote set-url ...
$ ./setup.py
```
