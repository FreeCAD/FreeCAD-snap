# freecad-ppd: Unofficial snap package for FreeCAD

> This is an unoffical package, so **do _not_ complain to upstream about issues with this snap!**

[![freecad-ppd](https://snapcraft.io/freecad-ppd/badge.svg)](https://snapcraft.io/freecad-ppd)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/freecad-ppd)

## About FreeCAD

FreeCAD is a parametric 3D modeler. Parametric modeling
allows you to easily modify your design by going back into
your model history and changing its parameters. FreeCAD is
open source (LGPL license) and completely modular, allowing
for very advanced extension and customization.

FreeCAD is multiplatfom, and reads and writes many open
file formats such as STEP, IGES, STL and others.

Visit the upstream project: https://www.freecad.org/ and https://github.com/FreeCAD/FreeCAD/

## Channels

There are three maintained channels for this snap:

- `stable` contains the latest upstream release, i.e. the most recent tagged commit. **Use this if you don't know what you're doing.**
- `edge` contains automated (daily) builds from the latest master commit. **Use this to test new features. Might be unstable.**
- `beta` contains automated weekly promotions from `edge`. **Use this if you want edge with fewer updates.**

## Apps/Commands

There are multiple apps/commands included in the snap:

- `freecad-ppd.freecad`:  Run FreeCAD
- `freecad-ppd.cmd`:      Run FreeCAD command line interface
- `freecad-ppd.pip`:      Install python packages for user (not system-wide). 
                          E.g. `freecad-ppd.pip install py_slvs` for Assembly3. 
                          
## FreeCAD Link Branch by RealThunder

There's also a snap that packages the well-known experimental FreeCAD fork by RealThunder: https://snapcraft.io/freecad-realthunder
Try it for some exciting new features and improvements.

[![freecad-realthunder](https://snapcraft.io/freecad-realthunder/badge.svg)](https://snapcraft.io/freecad-realthunder)

