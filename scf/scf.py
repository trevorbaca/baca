#! /usr/bin/env python
import baca


studio = baca.scf.StudioProxy()

try:
    studio.work_in_studio()
except EOFError:
    print '\n'
