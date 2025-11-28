# FreeCAD Snap Developer Documentation

## Recipes

### How to make a new stable release

* Create a PR that updates the `snap/snapcraft.yaml` file (see https://github.com/FreeCAD/FreeCAD-snap/pull/75 for example) and merge it to the stable branch
  **Result:** Once merged this will build a **candidate** release.
* Test the 'candidate' release. If no issues present then...
* Login to https://snapcraft.io/freecad/releases and promote the **candidate** release to **stable**
  **Result:** Stable will now be the latest stable branch

### How to update the Snap store credentials

This must be done once per year by someone with Maintainer access to this repo and the Snap Store login credentials. As of this writing, those people are @yorik, @luzpaz, and @chennes. On a Linux command line with `snapcraft` installed, generate new credentials with:

```shell
snapcraft export-login <credentials-filename>
```

Copy the contents of this file to the clipboard and go to the [FreeCAD-snap GitHub secrets page](https://github.com/FreeCAD/FreeCAD-snap/settings/secrets/actions). Edit the STORE_LOGIN secret to be the contents of the generated key.

### How to add snap-specific workarounds or changes

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

### How to trigger builds manually

The github action called 'Publish Daily' is an automated process that is triggered every evening to publish a new 'edge' build. It can also be triggered manually to build on-demand.

![Publish-Daily](assets/images/Snap-Publish-Daily.png)

In the screenshot above clicking the 'Run workflow' button will open a dialog with 2 buttons:

The `Branch:` button indicates what branch of FreeCAD-snap you'd like to trigger. Default is 'master'.

The green `Run workflow` button actually triggers the build to start. Once this is clicked, the build takes whatever time it takes to build FreeCAD from source and then push the new build to the 'edge' channel. After that all the user has to do is `snap refresh` and the latest 'edge' will auto-download to their machine

### Build snaps from FreeCAD branches or forks

It is possible to build snaps from any branch of fork of the FreeCAD repository. This option is also open to outside users that can simply make a PR to trigger and re-trigger a build.

1. Fork the FreeCAD-snap repo.
1. Create a new branch to work on.
1. Open *[snap/snapcraft.yaml](./snap/snapcraft.yaml)* in a text editor
1. Locate the `freecad` block of the yaml file
1. Modify the `source:` variable to reflect the specific fork of FreeCAD master to build. Note: must end with `.git` extension.
1. Add a  `source-branch:` variable to indicate what specific branch of said fork to build.  In the **example below** is a before and after in which we're building a snap of user @WandererFan's `hlrThreadrc1` branch from his FreeCAD clone ([borrowed from actual example](https://github.com/FreeCAD/FreeCAD-snap/pull/44)):

    ```yaml
     freecad:
      plugin: cmake
      source: https://github.com/FreeCAD/FreeCAD.git
    ```

    ```yaml
      freecad:
       plugin: cmake
       source: https://github.com/WandererFan/FreeCAD.git
       source-branch: hlrThreadrc1
    ```

1. Save the `snap/snapcraft.yaml` changes to the branch and make Pull Request to FreeCAD-snap.
1. Ask a maintainer to assign the https://github.com/FreeCAD/FreeCAD-snap/labels/safe%20to%20publish tag to the PR.
1. Result: the snap should build and output 'Installation Instructions'.
1. PR should be closed when said experimental snap builds aren't further necessary.
1. **Important note:** each commit to the branch will need a manual retrigger in order to re-build the snap. See below:

#### Triggering snap re-builds on PRs

As mentioned above, new commits to a branch will not retrigger the rebuilding of a snap. It needs to be done manually.

1. Open the same `snap/snapcraft.yaml` above
1. Find the `environment:` block
1. Add `BUILD_ME: 1` to the end of the block
1. Push change to the open PR
1. Note: To retrigger, iterate `BUILD_ME:`.
    ```yaml
    environment:
      LD_LIBRARY_PATH: $SNAP/usr/lib/   $SNAPCRAFT_ARCH_TRIPLET/blas:$SNAP/usr/lib/   $SNAPCRAFT_ARCH_TRIPLET/lapack # numpy
      LD_PRELOAD: $SNAP/usr/lib/    $SNAPCRAFT_ARCH_TRIPLET/libstubchown.so
      ...
      ...
      ...
      POVINI: $SNAP/etc/povray/3.7/povray.ini #     Raytracing
    ```

    ```yaml
      environment:
      LD_LIBRARY_PATH: $SNAP/usr/lib/   $SNAPCRAFT_ARCH_TRIPLET/blas:$SNAP/usr/lib/   $SNAPCRAFT_ARCH_TRIPLET/lapack # numpy
      LD_PRELOAD: $SNAP/usr/lib/    $SNAPCRAFT_ARCH_TRIPLET/libstubchown.so
      ...
      ...
      ...
      POVINI: $SNAP/etc/povray/3.7/povray.ini #     Raytracing
      BUILD_ME: 1
    ```
1. When task is complete and no more snap builds are needed, simply close the PR and delete the branch.

See example https://github.com/FreeCAD/FreeCAD-snap/pull/44

### Updating KDE Frameworks version

Every so often it is necessary to update the KDE Frameworks. See https://github.com/FreeCAD/FreeCAD-snap/pull/80.

This is related to the `kde-neon` extension, read the official documentation (may be outdated) https://snapcraft.io/docs/kde-neon-extension.

### Managing Dependencies in the FreeCAD Snap

The FreeCAD snap is built using a specific Ubuntu `coreNN` base, which means all its dependencies are sourced from either a specific core's version archive (`core22` at this time, which corresponds to **Ubuntu 22.04 (Jammy Jellyfish)**), or other package managers. There are three primary sources for adding dependencies, each with a specific purpose.

#### 1. Debian Packages (`apt`)

These are system-level libraries and tools sourced from the corresponding Ubuntu 22.04 archives and specified PPAs. This is the most common method for core C++ libraries and build tools.

*   **How to Find Packages:**
    1.  Search on the official Ubuntu Packages website: **[https://packages.ubuntu.com](https://packages.ubuntu.com)**.
    2.  **Ensure the correct distribution is selected** in your search to find the correct version.
    3.  You can cross-reference with [https://repology.org](https://repology.org) to see how packages are named across different systems.

*   **How to Add to `snapcraft.yaml`:**
    Dependencies are added to a part's definition under two distinct keys:
    *   `build-packages`: Packages required **only at build time** to compile the software (e.g., compilers, `-dev` header files). They are not included in the final snap.
        ```yaml
        parts:
          freecad:
            build-packages:
              - g++
              - libboost-all-dev
              - libxerces-c-dev
        ```
    *   `stage-packages`: The actual library files (`.so`, binaries, etc.) that are needed **at runtime**. These are bundled into the final snap.
        ```yaml
        parts:
          freecad:
            stage-packages:
              - libboost-filesystem1.74.0
              - libxerces-c3.2
              - python3-numpy
        ```

#### 2. Python Packages (`pip`)

For Python-specific dependencies, especially those not available in the Ubuntu archives or where a more recent version is required.

*   **How to Find Packages:**
    1.  The official source is the Python Package Index: **[https://pypi.org](https://pypi.org)**.

*   **How to Add to `snapcraft.yaml`:**
    These are listed under the `python-packages` key within a part that uses the `plugin: python`. For stability and reproducible builds, it is recommended to pin the version.
    ```yaml
    parts:
      python-packages:
        plugin: python
        python-packages:
          - ifcopenshell == 0.8.2  # BIM Workbench
          - opencamlib             # Path Workbench
          - scikit-sparse          # FEM Workbench
          - pip                    # Ensure pip is available inside the snap
    ```

Note: some Python packages might need some additional dependencies to be added to `stage-packages`
in order to run.

#### 3. Snap Dependencies (via `build-snaps`/`stage-snaps`)

This method bundles another snap's content, which is useful for providing a large, complex set of pre-built dependencies. In this project, it is limited to a single, purpose-built snap.

*   **How it's Used:**
    The `freecad-deps-core22` snap provides a curated set of libraries (OCCT) that are complex to build.
    *   `build-snaps`: Makes the content of the dependency snap available at build time (e.g., for linking against its libraries).
    *   `stage-snaps`: Primes the content of the dependency snap into our final snap at runtime.
*   **How to Add to `snapcraft.yaml`:**
    This is already configured and rarely needs to be changed, other than when updating to a new
    `coreNN` version.
    ```yaml
    parts:
      freecad:
        build-snaps:
          - freecad-deps-core22/candidate
        stage-snaps:
          - freecad-deps-core22/candidate
    ```

#### Deciding Between `apt` and `pip` for Python Libraries

When a Python library is available from both `apt` (e.g., `python3-numpy`) and `pip` (e.g., `numpy`), a decision must be made.

*   **Use the `apt` package (`stage-packages`) when:**
    *   **Stability is critical.** The Ubuntu archive version is fixed and heavily tested within the distribution.
    *   The package has complex non-Python system dependencies that are best resolved by `apt`.
    *   The version provided by Ubuntu 22.04 is sufficient and does not lack critical features or bug fixes.
    *   **Example:** `python3-numpy`, `python3-scipy`. These are core libraries that should be aligned with the system.

*   **Use the `pip` package (`python-packages`) when:**
    *   **A newer version is required** than what is available in Ubuntu 22.04. This is common for rapidly developing libraries or for accessing recent features and bug fixes.
    *   The package is not available in the Ubuntu archives at all.
    *   The package is pure Python with minimal system dependencies.
    *   **Example:** any package where the version on PyPI is far ahead of what's in Debian/Ubuntu, providing critical functionality for a specific workbench or FreeCAD's core.

## Architecture

### Dependencies

#### OpenCasCade (OCCT)

In order not to build OCCT on every FreeCAD snap build, it is built as a separate snap, only
manually on demand (e.g. when a new OCCT version is released, or required to support a feature or
to address a bug in FreeCAD). The snap including this dependency is published in the Snap Store,
and then pulled on the main FreeCAD snap as a `build-snaps` and/or `stage-snaps` dependency:

```yaml
# From https://github.com/FreeCAD/FreeCAD-snap/blob/cec4c973ad1241883f68fb1772b00fda0b0cfca3/snap/snapcraft.yaml#L153
    build-snaps:
      - freecad-deps-core22/candidate
    stage-snaps:
      - freecad-deps-core22/candidate
```

Development for the snap dependencies packaging happens on the main branch:

- https://github.com/FreeCAD/freecad-deps-snap/tree/master

Each snap `core` version is developed on its own branch:

- https://github.com/FreeCAD/freecad-deps-snap/tree/core22
- https://github.com/FreeCAD/freecad-deps-snap/tree/core24

> [!WARNING]
> Ideally, the worklow should be to have only the one https://github.com/FreeCAD/freecad-deps-snap
> repository, do development on the main branch, branch off each `coreNN` version it its own branch
> (as already done), and then publish directly each coreNN-versioned snap on the Snap store.
>
> However, it appears that the snap store only allows publishing from repositories, not from branches.
> This is the reason why there is also https://github.com/FreeCAD/freecad-deps-core22-snap: that's
> where currently the https://snapcraft.io/freecad-deps-core22 snap (see below) is published.
>
> As a workaround, the https://snapcraft.io/freecad-deps-core24 is published at this time directly
> from the main https://github.com/FreeCAD/freecad-deps-snap. This situation needs to be researched
> and the workflow cleaned up.

At the time, there are two versions of the dependencies snap available, depending on which Ubuntu
Core version the main snap is built on:

- https://snapcraft.io/freecad-deps-core22: For Ubuntu Core 22 (currently the default)
- https://snapcraft.io/freecad-deps-core24: For Ubuntu Core 24


#### GMSH

GMSH is also shipped in the same dependencies snap as OCCT.

#### Qt

Similarly to OCCT, Qt is too complex and extensive framework to build every time. In addition,
due to how Qt integrates in a host system in conjunction with snaps, it cannot simply be
installed from apt dependency packages.

The snap system provides its own way to ship Qt via extensions. The FreeCAD snap uses the
[`kde-neon` extension](https://documentation.ubuntu.com/snapcraft/stable/reference/extensions/kde-neon-extensions/). Some notes:

- We're using the `kde-neon` extension at the time, which is the one that supports `Qt 5` and is tied
  to `core22`
- This extension includes more than FreeCAD needs: it ships KDE and Qt. While FreeCAD would need only
  Qt, there is no Qt-only extension available at this time.
- The plan is to eventually migrate to `kde-neon-6` for a FreeCAD Qt 6 snap build, but there is an
  issue blocking this migration
- Crucially, `kde-neon` (and its `kde-neon-6` counterpart) are not very well maintained at this time.
  Yet there is no other alternative available
- This is the weakest point of the FreeCAD snap, as it depends on this very complex and virtually
  unmaintained extension. Contributing changes to it requires deep knowledge of the snapcraft code
  and the KDE ecosystem, none of which are well documented (or documented at all) in this specific area.

TBD: list the relevant repositories for the code related to this extension, and the relevant Snap Store packages

#### PySide

The `kde-neon` extensions ship only Qt, but not PySide. For PySide, we rely on apt packages from the KDE Neon archive. KDE Neon is based on Ubuntu LTS versions, but has newer packages for Qt available. This is how we'll be able to support Qt 6 in the `core24` snap. Without the KDE Neon packages, the Ubuntu 24.04 archive alone would not be able to provide the PySide6 packages, which were only included from Ubuntu 24.10 onwards.

> [!IMPORTANT]
> The PySide packages version must match the `major.minor` version of the Qt framework provided by the `kde-neon` extensions, otherwise FreeCAD won't work. This is another weak link, as we depend on two different upstreams to keep their versions in sync.

## Legacy user documentation

### Accessing 3rd-party devices (samba, usb etc..) via FreeCAD Snap

This user documentation section has been moved to the main [README.md](README.md) file. It has been left here to not break URLs linking to the original section location.

### Parallel Installs

This user documentation section has been moved to the main [README.md](README.md) file. It has been left here to not break URLs linking to the original section location.
