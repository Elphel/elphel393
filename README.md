# elphel393
Installation script for fetching and setting up building environment for elphel393 camera images,
it clones and configures several individual repositories, such as
* https://git.elphel.com/Elphel/linux-elphel
* https://git.elphel.com/Elphel/x393
* http://git.yoctoproject.org
* http://git.openembedded.org
* https://github.com/Xilinx/meta-xilinx
* https://git.elphel.com/Elphel/meta-elphel393

The same script pulls updates from these repositories

### Cloning

To have access to related Elphel's projects over **SSH** clone this project using **SSH**.

For **HTTPS** clone with **HTTPS**.

To change git protocol for all Elphel's projects - change the *remote* of this project accordingly, then run *setup.py*:
```sh
$ git remote -v
$ git remote set-url ...
$ ./setup.py
```

### Get environment
#### Dependencies
* poky might require installing some packages, please check with the [Yocto Poky Manual][1]
* extra requirement

```sh
$ sudo apt install python-numpy
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
* for more details, read [**this guide**][2] at [https://wiki.elphel.com][2]

[1]: http://www.yoctoproject.org/docs/2.0/mega-manual/mega-manual.html
[2]: http://wiki.elphel.com/index.php?title=Poky_2.0_manual

### Update and refresh environment
```sh
$ ./setup.py
```
### Rebuild targets
```sh
$ cd poky
$ . ./oe-init-build-env
$ (if changes in the kernel) bitbake linux-xlnx -c link -f
$ (if changes in the rootfs and the kernel) bitbake core-image-elphel393
```

