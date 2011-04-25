from abjad import *
from baca.rhythm.kaleids import *


def test_baca_rhythm_kaleids_PartFilledChunksWithPatternFilledTokens_01( ):

   pattern, denominator, prolation_addenda = [1], 16, [2]
   lefts, middles, rights = [0], [-1], [0]
   left_lengths, right_lengths = [1], [1]
   kaleid = PartForcedChunkWithPatternFilledTokens(
      pattern, denominator, prolation_addenda,
      lefts, middles, rights, left_lengths, right_lengths)

   duration_tokens = [(3, 16), (3, 8)]
   music = kaleid(duration_tokens)

   music = seqtools.flatten_sequence(music)
   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, music)

   r'''
   \new Staff {
      {
         \time 3/16
         \fraction \times 3/5 {
            c'16
            r16
            r16
            r16
            r16
         }
      }
      {
         \time 3/8
         \fraction \times 3/4 {
            r16
            r16
            r16
            r16
            r16
            r16
            r16
            c'16
         }
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\t\\fraction \\times 3/5 {\n\t\t\tc'16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tr16\n\t\t\tc'16\n\t\t}\n\t}\n}"


def test_baca_rhythm_kaleids_PartFilledChunksWithPatternFilledTokens_02( ):

   pattern, denominator, prolation_addenda = [1], 4, [2]
   lefts, middles, rights = [-1], [0], [-1]
   left_lengths, right_lengths = [1], [1]
   kaleid = PartForcedChunkWithPatternFilledTokens(
      pattern, denominator, prolation_addenda,
      lefts, middles, rights, left_lengths, right_lengths)

   duration_tokens = [(3, 16), (3, 8)]
   music = kaleid(duration_tokens)

   music = seqtools.flatten_sequence(music)
   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, music)

   r'''
   \new Staff {
      {
         \time 3/16
         \fraction \times 3/5 {
            r4
            c'16
         }
      }
      {
         \time 3/8
         \fraction \times 3/4 {
            c'8.
            c'4
            r16
         }
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\t\\fraction \\times 3/5 {\n\t\t\tr4\n\t\t\tc'16\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\t\\fraction \\times 3/4 {\n\t\t\tc'8.\n\t\t\tc'4\n\t\t\tr16\n\t\t}\n\t}\n}"
