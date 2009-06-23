data_driver_template = '''#! /usr/bin/env python

from helpers import %s
import baca
import os

if __name__ == '__main__':

   os.system('clear')

   print '%s'
   output = %s( )
   output = '%s = %%s' %% output 
   baca.utilities.cache_output(output, '%s', __file__)
   print \'\''''
