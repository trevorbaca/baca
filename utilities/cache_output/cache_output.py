import os


def cache_output(output, name, location):
   '''Cache string-based output to location/../../output directory.'''

   assert isinstance(output, str)
   assert isinstance(name, str)
   assert not ' ' in name

   filename = os.path.abspath(location)
   dirname = os.path.dirname(filename)
   dirpath = dirname.split(os.sep)
   parpardir = dirpath[:-2]
   parpardir.insert(0, '/')
   parpardir.append('output')
   output_directory = os.path.join(*parpardir)
   outfile = os.path.join(output_directory, name + '.py')
   outfile = file(outfile, 'w')
   outfile.write(output)
   outfile.close( )
