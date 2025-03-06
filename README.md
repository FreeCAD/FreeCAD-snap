# Snap package for FreeCAD [![Publish Daily](https://github.com/FreeCAD/FreeCAD-snap/actions/workflows/publish-daily.yml/badge.svg)](https://github.com/FreeCAD/FreeCAD-snap/actions/workflows/publish-daily.yml)

Source code repository for distributing FreeCAD on Linux using the [snap packaging format](https://snapcraft.io/docs).

If you are just looking for a way to get FreeCAD on your Linux-based OS, you can skip to the installation:

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/freecad)

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

![Stable version](https://img.shields.io/snapcraft/v/freecad/latest/stable?label=stable&color=1c862c) ![Edge version](https://img.shields.io/snapcraft/v/freecad/latest/edge?label=edge&color=gold) ![Beta version](https://img.shields.io/snapcraft/v/freecad/latest/beta?label=beta&color=gold) ![Candidate Version](https://img.shields.io/snapcraft/v/freecad/latest/candidate?label=candidate&color=gold)


There are multiple maintained channels for this snap:

- `stable` contains the latest upstream release, i.e. the most recent tagged commit. **Use this if you don't know what you're doing.**
- `edge` contains automated (daily) builds from the latest master commit. **Use this to test new features. Might be unstable.**
- `beta` contains automated weekly promotions from `edge`. **Use this if you want edge with fewer updates.**
- `candidate` contains release candidate (RC) builds. **Use this if you want to test release candidates before a major release.**

## Apps/Commands

There are multiple apps/commands included in the snap:

- `freecad.freecad`:  Run FreeCAD
- `freecad.cmd`:      Run FreeCAD command line interface
- `freecad.pip`:      Install python packages for user (not system-wide).
                      E.g. `freecad.pip install py_slvs` for Assembly3.

## FreeCAD Link Branch by RealThunder

There's also a snap that packages the well-known experimental FreeCAD fork by RealThunder: https://snapcraft.io/freecad-realthunder
Try it for some exciting new features and improvements.

[![freecad-realthunder](https://snapcraft.io/freecad-realthunder/badge.svg)](https://snapcraft.io/freecad-realthunder)
