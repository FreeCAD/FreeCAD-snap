# Snap package for FreeCAD [![Publish Daily](https://github.com/FreeCAD/FreeCAD-snap/actions/workflows/publish-daily-qt5.yml/badge.svg)](https://github.com/FreeCAD/FreeCAD-snap/actions/workflows/publish-daily-qt5.yml)

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


There are multiple installation [channels](https://snapcraft.io/docs/channels) for this snap:

- `stable` contains the latest upstream release, i.e. the most recent tagged commit. **Use this if you don't know what you're doing.**
- `edge` contains automated (daily) builds from the latest master commit. **Use this to test new features. Might be unstable.**
- `beta` contains automated weekly promotions from `edge`. **Use this if you want edge with fewer updates.**
- `candidate` contains release candidate (RC) builds. **Use this if you want to test release candidates before a major release.**

## Apps/Commands

There are multiple apps/commands included in the snap:

- `freecad.freecad`:  Run FreeCAD, can be executed simply as `freecad`
- `freecad.cmd`:      Run FreeCAD command line interface
- `freecad.pip`:      Install python packages for user (not system-wide).
                      E.g. `freecad.pip install py_slvs` for Assembly3.

## Accessing 3rd-party devices (samba, usb etc..) via FreeCAD Snap

```shell
sudo snap connect freecad:removable-media
```
Reference: https://askubuntu.com/questions/1226304/how-do-i-access-mounted-hard-drive-with-a-snap-application

## Parallel Installs

Running multiple snaps AKA 'Parallel Installs' (parallel but separate).

By default, snap packages that have several 'channels' will share configs between them. For testing purposes sometimes this isn't wanted, the solution per the snapcraft docs is using the [parallel install](https://snapcraft.io/docs/parallel-installs) feature.

> Parallel installs enable you to run multiple instances of the same snap on the same system. Each instance is completely isolated from all other instances, including its name, configuration, interface connections, data locations, services, applications and aliases.

Note: at the time of writing the parallel install feature is still considered experimental.

In the context of FreeCAD, this feature can be useful for example if there are experimental changes (in an experimental build) to the FreeCAD config files that could corrupt the snap stable or snap edge channel FreeCAD config files.

Example: Install edge snap in parallel to the stable snap

```shell
# Enable experimental parallel instances feature. You only need to do this once
$ sudo snap set system experimental.parallel-instances=true
```

```shell
# Install freecad snap from channel edge as 'freecad_edge'
$ sudo snap install freecad_edge --channel=edge
# run FreeCAD from this parallel install
$ freecad_edge
```
