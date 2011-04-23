from abjad import *
from baca.rhythm.kaleids import *


def test_baca_kaleids_BigEndianRestMaker_01( ):
   '''Fine note-value signal.
   '''

   rest_maker = BigEndianRestMaker( )

   duration_tokens = [(5, 16), (3, 8)]
   leaf_lists = rest_maker(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/16
         r4
         r16
      }
      {
         \time 3/8
         r4.
      }
   }
   '''

   assert staff.format == '\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tr4\n\t\tr16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tr4.\n\t}\n}'
