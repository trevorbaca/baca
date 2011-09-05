# -*- encoding: utf-8 -*-
from score_package_dictionary import score_package_dictionary
from score_package_number_to_score_package_name import score_package_number_to_score_package_name


def run_score_selection_menu():

   print 'Please select from the following:'
   print ''

   score_package_numbers = []
   items = score_package_dictionary.items()
   for score_package_number, (score_package_name, score_title) in sorted(items):
      score_package_numbers.append(score_package_number)
      print '%5s: %s' % (score_package_number, score_title)

   print ''

   while True:
      score_package_number = raw_input('scf> ')
      score_package_number = int(score_package_number)
      if score_package_number in score_package_numbers:
         break

   score_package_name = score_package_number_to_score_package_name(score_package_number)

   return score_package_name
