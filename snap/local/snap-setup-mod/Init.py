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

def configure_mod_render():
  import FreeCAD
  param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Render")
  if not param.GetString("LuxCorePath", ""):
    param.SetString("LuxCorePath", "/snap/freecad/current/usr/bin/luxcoreui")
  if not param.GetString("LuxCoreConsolePath", ""):
    param.SetString("LuxCoreConsolePath", "/snap/freecad/current/usr/bin/luxcoreconsole")

def fix_theme():
  import FreeCAD
  param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Bitmaps/Theme")
  if param.GetBool("ThemeSearchPaths", False)  != param.GetBool("ThemeSearchPaths", True):
    param.SetBool("ThemeSearchPaths", False)

add_snap_pythonpath()
configure_mod_mesh()
configure_mod_render()
fix_theme()
