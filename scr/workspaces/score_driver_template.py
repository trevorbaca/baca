score_driver_template = '''#! /usr/bin/env python

from abjad.tools import io
from helpers import %s
import baca
import os
import sys


if __name__ == '__main__':

    os.system('clear')
    usage = 'usage: run.py [--nowrite|--write]'
    write = baca.util.check_score_builder_commandline(sys.argv, usage)
    dirname = os.path.abspath(os.path.dirname(__file__))
    template = os.path.join(dirname, 'templates', 'template.ly')

    print '%s'
    score = %s()
    name = os.path.join(dirname, 'scores', '%s')
    title = []
    io.write_and_show(score, name, template, title, write = write)
    print ''
'''
