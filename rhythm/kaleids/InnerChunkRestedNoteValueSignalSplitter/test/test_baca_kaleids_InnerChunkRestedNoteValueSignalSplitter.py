from abjad import *
from baca.rhythm.kaleids import *


def test_baca_kaleids_InnerChunkRestedNoteValueSignalSplitter_01( ):
   '''Fine note-value signal.
   '''

   nvs, denominator = [1], 16
   rested_splitter = InnerChunkRestedNoteValueSignalSplitter(nvs, denominator)

   duration_tokens = [(3, 16), (3, 8)]
   leaf_lists = rested_splitter(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 3/16
         c'16
         r16
         r16
      }
      {
         \time 3/8
         r16
         r16
         r16
         r16
         r16
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'16\n\t\tr16\n\t\tr16\n\t}\n\t{\n\t\t\\time 3/8\n\t\tr16\n\t\tr16\n\t\tr16\n\t\tr16\n\t\tr16\n\t\tc'16\n\t}\n}"


def test_baca_kaleids_InnerChunkRestedNoteValueSignalSplitter_02( ):
   '''Corase note-value signal.
   '''

   nvs, denominator = [1], 4
   rested_splitter = InnerChunkRestedNoteValueSignalSplitter(nvs, denominator)

   duration_tokens = [(3, 16), (3, 8)]
   leaf_lists = rested_splitter(duration_tokens)
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
         r16
         r4
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8.\n\t}\n\t{\n\t\t\\time 3/8\n\t\tr16\n\t\tr4\n\t\tc'16\n\t}\n}"
