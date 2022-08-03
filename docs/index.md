# FreeCAD Snap Documentation

## How to add snap-specific workarounds or changes

Edit [snap/local/snap-setup-mod/Init.py](https://github.com/FreeCAD/FreeCAD-snap/blob/master/snap/local/snap-setup-mod/Init.py), which is called on every start of FreeCAD.

E.g.

```python
def configure_mod_raytracing():
  import FreeCAD
  param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing")
  if not param.GetString("PovrayExecutable", ""):
    param.SetString("PovrayExecutable", "/snap/freecad/current/usr/bin/povray")

configure_mod_raytracing()
```

This automatically sets the `PovrayExecutable` parameter to the correct path inside the snap.

**Convention**: One function per workbench, don't overwrite the user's settings.

## Publishing Daily

The github action called 'Publish Daily' is an automated process that is triggered every evening to publish a new 'edge' build. It can also be triggered manually to build on-demand. 

![Publish-Daily](assets/images/Snap-Publish-Daily.png)

In the screenshot above clicking the 'Run workflow' button will open a dialog with 2 buttons:

The `Branch:` button indicates what branch of FreeCAD-snap you'd like to trigger. Default is 'master'.

The green `Run workflow` button actually triggers the build to start. Once this is clicked, the build takes whatever time it takes to build FreeCAD from source and then push the new build to the 'edge' channel. After that all the user has to do is `snap refresh` and the latest 'edge' will auto-download to their machine


## Publishing to Branch

There is an option to build Snaps from experimental commits, branches, or even git release tags. 

**Note:** It is possible to create experimental builds from any true fork of the upstream FreeCAD repository ([ref](https://github.com/FreeCAD/FreeCAD/pull/7118#issuecomment-1171458436))

![Publish-to-Branch](assets/images/Snap-Publish-to-Branch-screenshot.png)

In the the screenshot above the first field labeled **`FreeCAD commit/branch/tag`** is able to receive the following inputs:  

* **`commit`** this is a specific git hash of an open Pull Request in FreeCAD/FreeCAD  
* **`branch`** is for special FreeCAD/FreeCAD branches one would like to compile. Simply adding the name of said branch is enough. For example: 'Toponaming' (note branch should exist first).
* **`tag`** is for building snaps from a specific FreeCAD/FreeCAD release tag. 

The secound field in the above screenshot **`Snapcraft branch`** is simply the unique build name you can grant to this specific build. 

Then simply pressing the **Run workflow** button will trigger said build. When build is complete, the method to install this build is simple. In the CLI invoke:  
```shell
snap install freecad --channel <experimental-build-name>
```

When you're done testing the build, to return to the original build you were running just swap out the build name and refresh; for example: `stable` or `edge` 
```shell
snap refresh freecad --channel edge
```

## Parallel Installs

Running multiple snaps AKA 'Parallel Installs' (parallel but separate).

By default, snap packages that have several 'channels' will share configs between them. For testing purposes sometimes this isn't wanted, the solution per the snapcraft docs is using the [parallel install](https://snapcraft.io/docs/parallel-installs) feature. 

> Parallel installs enable you to run multiple instances of the same snap on the same system. Each instance is completely isolated from all other instances, including its name, configuration, interface connections, data locations, services, applications and aliases.

Note: at the time of writing this the parallel install feature is still considered experimental

In the context of FreeCAD, this feature would be useful for example if there are experimental changes (in an experimental build) to the FreeCAD config files that could corrupt the snap stable or snap edge channel FreeCAD config files.   

Example: Install edge snap in parallel to the stable snap

```shell
# Enable experimental parallel instances feature
$ sudo snap set system experimental.parallel-instances=true
# Install freecad snap from channel edge as 'freecad_edge'
$ sudo snap install freecad_edge --channel=edge
# run FreeCAD from this parallel install
$ freecad_edge