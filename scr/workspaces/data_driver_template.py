data_driver_template = '''#! /usr/bin/env python

from abjad.tools import iotools
from helpers import %s
import baca
import os
import pprint

if __name__ == '__main__':

    iotools.clear_terminal()

    print '%s'
    output = %s()
    output = pprint.pformat(output)
    output = '%s = %%s' %% output
    baca.util.cache_output(output, '%s', __file__)
    print \'\''''
