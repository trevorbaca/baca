import os


def cache_output(output, name, location):
   '''Cache string-based output to output directory relative to location.'''

   assert isinstance(output, str)
   assert isinstance(name, str)
   assert not ' ' in name

   dirname = os.path.abspath(location)
   dirname = os.path.dirname(dirname)
   outfile = os.path.join(dirname, 'output', name + '.py')
   outfile = file(outfile, 'w')
   outfile.write(output)
   outfile.close( )
