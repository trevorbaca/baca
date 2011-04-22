from abjad import *
from baca.rhythm.kaleids import *


## trivial global definition
def preprocessor(signal, seeds):
   return signal


def test_baca_rhythm_kaleids_ProlatedNoteValueSignalSplitter_01( ):
   '''Prolate and split coarse signal.
   '''

   nvs, denominator, prolation = [-1, 5], 4, [6]
   prolated_splitter = ProlatedNoteValueSignalSplitter(nvs, denominator, preprocessor, prolation, preprocessor)

   duration_pairs = [(2, 8), (5, 8)]
   tuplets = prolated_splitter(duration_pairs, [ ])

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
   measuretools.replace_contents_of_measures_in_expr(staff, tuplets)

   r'''
   \new Staff {
      {
         \time 2/8
         {
            r4
         }
      }
      {
         \time 5/8
         \fraction \times 5/6 {
            c'2.
         }
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n\t{\n\t\t\\time 5/8\n\t\t\\fraction \\times 5/6 {\n\t\t\tc'2.\n\t\t}\n\t}\n}"


def test_baca_rhythm_kaleids_ProlatedNoteValueSignalSplitter_02( ):
   '''Split fine signal.
   '''

   nvs, denominator, prolation = [-1, 5], 16, [6]
   prolated_splitter = ProlatedNoteValueSignalSplitter(nvs, denominator, preprocessor, prolation, preprocessor)

   duration_pairs = [(2, 8), (5, 8)]
   tuplets = prolated_splitter(duration_pairs, [0, 0])

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
   measuretools.replace_contents_of_measures_in_expr(staff, tuplets)

   r'''
   \new Staff {
      {
         \time 2/8
         {
            r16
            c'8.
         }
      }
      {
         \time 5/8
         \fraction \times 5/6 {
            c'8
            r16
            c'4
            c'16
            r16
            c'8.
         }
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t{\n\t\t\tr16\n\t\t\tc'8.\n\t\t}\n\t}\n\t{\n\t\t\\time 5/8\n\t\t\\fraction \\times 5/6 {\n\t\t\tc'8\n\t\t\tr16\n\t\t\tc'4\n\t\t\tc'16\n\t\t\tr16\n\t\t\tc'8.\n\t\t}\n\t}\n}"
