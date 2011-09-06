#! /usr/bin/env python

import baca
import io
import sys


score_package_name = io.handle_startup(sys.argv)
score_package_proxy = baca.scf.ScorePackageProxy(score_package_name)
try:
    score_package_proxy.manage_score()
except EOFError:
    print '\n'
