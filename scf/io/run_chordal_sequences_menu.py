from check_and_make_directory import check_and_make_directory
from get_score_title import get_score_title
from inspect_chordal_sequence import inspect_chordal_sequence
from list_chordal_sequences import list_chordal_sequences
from make_chordal_sequence import make_chordal_sequence
from present_menu import present_menu
import os


def run_chordal_sequences_menu(score_package_name):

   score_package_directory = os.environ.get(score_package_name.upper( ))
   path_parts = (score_package_directory, 'mus', 'materials', 'chordal_sequences')
   chordal_sequences_directory = os.path.join(*path_parts)
   if not check_and_make_directory(chordal_sequences_directory):
      return

   os.system('clear')
   score_title = get_score_title(score_package_name)

   while True:
      print '%s - chordal sequences' % score_title
      print ''
      chordal_sequences = list_chordal_sequences(score_package_name)
      if not chordal_sequences:
         print '  No chordal sequences found.'
      additional_pairs = [('m', 'make new chordal sequence')]
      choice, value = present_menu(chordal_sequences, additional_pairs)
      try:
         chordal_sequence_number = int(choice)
         try:
            inspect_chordal_sequence(score_package_name, chordal_sequence_number)
         except KeyboardInterrupt:
            os.system('clear')
      except ValueError:
         if choice.lower( ) == 'm':
            try:
               make_chordal_sequence(score_package_name)
            except KeyboardInterrupt:
               os.system('clear')
         elif choice.lower( ) == 'r':
            os.system('clear')
            break
         elif choice.lower( ) == 'q':
            raise SystemExit
         else:
            raise ValueError('unknown choice "%s".' % choice)

   os.system('clear')
