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