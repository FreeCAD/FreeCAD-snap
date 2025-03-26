def add_snap_pythonpath():
  import os
  import sys

  pythonpath = os.environ.get("SNAP_PYTHONPATH")
  if pythonpath:
    print(f"Adding snap-specific PYTHONPATH to sys.path: {pythonpath}")
    os.environ["PYTHONPATH"] = pythonpath
    for path in pythonpath.split(":"):
      sys.path.insert(0, path)

def configure_mod_mesh():
  import FreeCAD
  param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Mesh/Meshing")
  if not param.GetString("gmshExe", ""):
    param.SetString("gmshExe", "/snap/freecad/current/usr/bin/gmsh")

def fix_theme():
  import FreeCAD
  param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Bitmaps/Theme")
  if param.GetBool("ThemeSearchPaths", False)  != param.GetBool("ThemeSearchPaths", True):
    param.SetBool("ThemeSearchPaths", False)

def fix_wayland():
  '''Temporary workaround to reset the QT_QPA_PLATFORM environment variable,
  so that FreeCAD does not run on Wayland, which Coin3D does not yet support.
  See known issues on https://github.com/FreeCAD/FreeCAD-snap/pull/179'''
  import os

  qtqpaplatformXcb = "xcb"
  qtqpaplatform = os.environ.get("QT_QPA_PLATFORM")
  if qtqpaplatform:
    print(f"Resetting QT_QPA_PLATFORM environment variable from {qtqpaplatform} to '{qtqpaplatformXcb}'")
    os.environ["QT_QPA_PLATFORM"] = qtqpaplatformXcb

add_snap_pythonpath()
configure_mod_mesh()
fix_theme()
# fix_wayland()
