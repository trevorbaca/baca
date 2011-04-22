from abjad import *
from baca.rhythm.kaleids import *


## global for test functions in this module
def signal_preprocessor(signal, seeds):
   voice_index, measure_index = seeds
   result = seqtools.rotate_sequence(signal, -voice_index * len(signal) // 4)
   result = seqtools.rotate_sequence(result, -measure_index * 4)
   return type(signal)(result)


def test_baca_rhythm_kaleids_NoteValueSignalSplitter_01( ):
   '''Split fine signal.
   '''

   signal, denominator_of_signal = [-1, 5], 16
   splitter = NoteValueSignalSplitter(signal, denominator_of_signal, signal_preprocessor)

   duration_pairs = [(2, 8), (5, 8)]
   leaf_lists = splitter(duration_pairs, [0, 0])
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 2/8
         r16
         c'8.
      }
      {
         \time 5/8
         c'8
         r16
         c'4
         c'16
         r16
         c'16
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tr16\n\t\tc'8.\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'8\n\t\tr16\n\t\tc'4\n\t\tc'16\n\t\tr16\n\t\tc'16\n\t}\n}"


def test_baca_rhythm_kaleids_NoteValueSignalSplitter_02( ):
   '''Split coarse signal.
   '''

   signal, denominator_of_signal = [-1, 5], 4
   splitter = NoteValueSignalSplitter(signal, denominator_of_signal, signal_preprocessor)

   duration_pairs = [(2, 8), (5, 8)]
   leaf_lists = splitter(duration_pairs, [0, 0])
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 2/8
         r4
      }
      {
         \time 5/8
         c'2
         c'8
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tr4\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n}"
