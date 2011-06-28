from check_and_make_directory import check_and_make_directory
from make_chordal_sequence import make_chordal_sequence
import os

def run_chordal_sequences_menu(score_package_name):

   score_package_directory = os.environ.get(score_package_name.upper( ))
   path_parts = (score_package_directory, 'mus', 'materials', 'chordal_sequences')
   chordal_sequences_directory = os.path.join(*path_parts)
   if not check_and_make_directory(chordal_sequences_directory):
      return

   while True:
      if os.listdir(chordal_sequences_directory):
         print 'Score contains chordal sequences.'
      else:
         print 'Score contains no chordal sequences.'
      print ''
      print '  [m: make new chordal sequence ...]'
      print '  r: return to previous menu'
      print ''
      input = raw_input('scf> ')
      print ''
      if input.lower( ) == 'm':
         make_chordal_sequence(score_package_name)
      elif input.lower( ) == 'r':
         break
