# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the FreeCAD project.


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

def configure_mod_fem_solvers():
  """
  Sets the default path for the Elmer FEM solvers if they are not already set.
  This ensures FreeCAD's FEM workbench can find the Elmer binaries that are
  bundled within the snap.
  """
  import FreeCAD
  param_group = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Elmer")

  # --- Configure ElmerSolver ---
  if not param_group.GetString("elmerBinaryPath", ""):
    param_group.SetString("elmerBinaryPath", "/snap/freecad/current/usr/bin/ElmerSolver")

  # --- Configure ElmerGrid ---
  if not param_group.GetString("gridBinaryPath", ""):
    param_group.SetString("gridBinaryPath", "/snap/freecad/current/usr/bin/ElmerGrid")

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
configure_mod_fem_solvers()
fix_theme()
# fix_wayland()
