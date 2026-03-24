// SPDX-License-Identifier: LGPL-2.1-or-later
// SPDX-FileNotice: Part of the FreeCAD project.

#include <sys/types.h>
#include <stdio.h>

int chown(const char *pathname,
          uid_t owner,
          gid_t group)
{
  fprintf(stderr, "stub-chown: Stubbed out attempt to chown '%s'\n", pathname);
  return 0;
}
