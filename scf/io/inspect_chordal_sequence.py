from get_chordal_sequence_data import get_chordal_sequence_data
from get_chordal_sequences_directory import get_chordal_sequences_directory
#from get_score_title import get_score_title
from list_chordal_sequences import list_chordal_sequences
from open_chordal_sequence_pdf import open_chordal_sequence_pdf
import os
import pprint


def inspect_chordal_sequence(score_package_name, chordal_sequence_number):

   score_title = get_score_title(score_package_name)
   path = get_chordal_sequences_directory(score_package_name)
   chordal_sequences = list_chordal_sequences(score_package_name)
   
   if len(chordal_sequences) < chordal_sequence_number:
      raise ValueError('score contains only %s chordal sequences.' % len(chordal_sequences))

   os.system('clear')
   print '%s - chordal sequences - %s' % (score_title, chordal_sequence_number)
   print ''

   print '  d: data      p: pdf       v: rename     x: delete'
   print ''

   while True:
      choice = raw_input('scf> ')
      if choice.lower( ) == 'd':
         chordal_sequence_data = get_chordal_sequence_data(score_package_name, chordal_sequence_number)
         pprint.pprint(chordal_sequence_data)
         print ''
      elif choice.lower( ) == 'p':
         open_chordal_sequence_pdf(score_package_name, chordal_sequence_number)
         print ''
      elif choice.lower( ) == 'q':
         raise SystemExit
      elif choice.lower( ) == 'r':
         break
      elif choice.lower( ) == 'v':
         rename_material_package(score_package_name, materials_package_name)
      elif choice.lower( ) == 'x':
         delete_material_package(score_package_name, materials_package_name)

   os.system('clear')
