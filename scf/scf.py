#! /usr/bin/env python

import baca
import io
import sys


score_package_name = io.handle_startup(sys.argv)
#io.profile_score_directory(score_package_name)
#io.run_main_menu(score_package_name)
score_package_proxy = baca.scf.ScorePackageProxy(score_package_name)
score_package_proxy.run_score_package_proxy_startup_interface( )
