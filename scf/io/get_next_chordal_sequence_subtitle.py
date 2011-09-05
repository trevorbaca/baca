from get_verified_user_input import get_verified_user_input
from list_chordal_sequences import list_chordal_sequences


def get_next_chordal_sequence_subtitle(score_package_name):

   chordal_sequences = list_chordal_sequences(score_package_name)
   total_chordal_sequences = len(chordal_sequences)
   next_number = total_chordal_sequences + 1
   subtitle = 'chordal sequence %s' % next_number

#   print "Default subtitle is '%s'." % subtitle
#   print ''
#   input = raw_input('Use default subtitle? ')
#   print ''
#
#   if input.lower() in ('2', 'n', 'no'):
#      subtitle = get_verified_user_input('Enter new subtitle> ')

   return subtitle
