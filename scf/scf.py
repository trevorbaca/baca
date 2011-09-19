#! /usr/bin/env python

import baca
#import io
#import sys


#score_package_name, command_string = io.handle_startup(sys.argv)
#score_package_proxy = baca.scf.ScorePackageProxy(score_package_name)
#try:
#    score_package_proxy.manage_score(command_string = command_string)
#except EOFError:
#    print '\n'

studio = baca.scf.StudioProxy()

try:
    studio.work_in_studio()
except EOFError:
    print '\n'
