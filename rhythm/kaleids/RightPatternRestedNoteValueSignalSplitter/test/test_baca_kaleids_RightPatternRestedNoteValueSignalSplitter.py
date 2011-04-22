from abjad import *
from baca.rhythm.kaleids import *


def test_baca_kaleids_RightPatternRestedNoteValueSignalSplitter_01( ):
   '''Fine note-value signal.
   '''

   nvs, denominator, rs = [1], 16, [4]
   rested_splitter = RightPatternRestedNoteValueSignalSplitter(nvs, denominator, rs)

   duration_tokens, seeds = [(3, 16), (3, 8)], [ ]
   leaf_lists = rested_splitter(duration_tokens, seeds)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 3/16
         c'16
         c'16
         c'16
      }
      {
         \time 3/8
         r16
         c'16
         c'16
         c'16
         r16
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tr16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tr16\n\t\tc'16\n\t}\n}"


def test_baca_kaleids_RightPatternRestedNoteValueSignalSplitter_02( ):
   '''Corase note-value signal.
   '''

   nvs, denominator, rs = [1], 4, [4]
   rested_splitter = RightPatternRestedNoteValueSignalSplitter(nvs, denominator, rs)

   duration_tokens, seeds = [(3, 16), (3, 8)], [ ]
   leaf_lists = rested_splitter(duration_tokens, seeds)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 3/16
         c'8.
      }
      {
         \time 3/8
         c16
         c'4
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8.\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'16\n\t\tc'4\n\t\tc'16\n\t}\n}"
