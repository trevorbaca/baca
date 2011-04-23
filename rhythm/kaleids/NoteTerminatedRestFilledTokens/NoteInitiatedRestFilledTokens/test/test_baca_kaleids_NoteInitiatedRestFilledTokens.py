from abjad import *
from baca.rhythm.kaleids import *


def test_baca_kaleids_NoteInitiatedRestFilledTokens_01( ):
   '''Fine note-value signal.
   '''

   numerators, denominator = [2, 1], 16
   kaleid = NoteInitiatedRestFilledTokens(numerators, denominator)

   duration_tokens = [(5, 16), (3, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)
   f(staff)

   r'''
   \new Staff {
      {
         \time 5/16
         c'8
         r8.
      }
      {
         \time 3/8
         c'16
         r4
         r16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tc'8\n\t\tr8.\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'16\n\t\tr4\n\t\tr16\n\t}\n}"


def test_baca_kaleids_NoteInitiatedRestFilledTokens_02( ):
   '''Coarse note-value signal.
   '''

   numerators, denominator = [2, 1], 4
   kaleid = NoteInitiatedRestFilledTokens(numerators, denominator)

   duration_tokens = [(5, 16), (3, 8)] 
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/16
         c'4
         c'16
      }
      {
         \time 3/8
         c'4
         r8
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tc'4\n\t\tc'16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'4\n\t\tr8\n\t}\n}"
