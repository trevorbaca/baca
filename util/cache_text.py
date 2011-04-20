from baca.util.get_parent_directory import get_parent_directory
import os


def cache_text(text, text_file_name, location):
   '''Cache `text` string to text file with name equal to
   `text_file_name` in ../_txt directory.
   '''

   assert isinstance(text, str)
   assert isinstance(text_file_name, str)
   assert not ' ' in text_file_name

   parent_directory = get_parent_directory(location)
   text_directory = os.path.join(parent_directory, '_txt')
   outfile = os.path.join(text_directory, text_file_name + '.txt')
   outfile = file(outfile, 'w')
   outfile.write(text)
   outfile.close( )
