from abjad import *
from baca.rhythm.kaleids import *


def test_baca_kaleids_NoteWrappedRestFilledTokens_01( ):
   '''Fine note-value signal.
   '''

   numerators, denominator = [2, 1], 16
   kaleid = NoteWrappedRestFilledTokens(numerators, denominator)

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
         r8
         c'16
      }
      {
         \time 3/8
         c'8
         r8.
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tc'8\n\t\tr8\n\t\tc'16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'8\n\t\tr8.\n\t\tc'16\n\t}\n}"


def test_baca_kaleids_NoteWrappedRestFilledTokens_02( ):
   '''Coarse note-value signal.
   '''

   numerators, denominator = [2, 1], 4
   kaleid = NoteWrappedRestFilledTokens(numerators, denominator)

   duration_tokens = [(5, 16), (3, 8)] 
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/16
         c'16
         c'4
      }
      {
         \time 3/8
         c'4.
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tc'16\n\t\tc'4\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'4.\n\t}\n}"
