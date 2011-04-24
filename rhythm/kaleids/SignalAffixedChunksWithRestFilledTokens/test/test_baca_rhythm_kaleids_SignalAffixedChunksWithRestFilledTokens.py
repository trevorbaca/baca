from abjad import *
from baca.rhythm.kaleids import *


def test_baca_rhythm_kaleids_SignalAffixedChunksWithRestFilledTokens_01( ):

   prefix_signal, prefix_denominator, prefix_lengths = [1], 4, [2]
   suffix_signal, suffix_denominator, suffix_lengths = [3], 32, [4]
   kaleid = SignalAffixedChunksWithRestFilledTokens(
      prefix_signal, prefix_denominator, prefix_lengths,
      suffix_signal, suffix_denominator, suffix_lengths)

   duration_tokens = [(5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         c'4
         c'4
         r8
      }
      {
         \time 5/8
         r2
         r8
      }
      {
         \time 5/8
         r4
         c'16.
         c'16.
         c'16.
         c'16.
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tc'16.\n\t\tc'16.\n\t\tc'16.\n\t\tc'16.\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedChunksWithRestFilledTokens_02( ):

   prefix_signal, prefix_denominator, prefix_lengths = [1], 4, [20]
   suffix_signal, suffix_denominator, suffix_lengths = [1], 4, [2]
   kaleid = SignalAffixedChunksWithRestFilledTokens(
      prefix_signal, prefix_denominator, prefix_lengths,
      suffix_signal, suffix_denominator, suffix_lengths)

   duration_tokens = [(5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         c'4
         c'4
         c'8
      }
      {
         \time 5/8
         r2
         r8
      }
      {
         \time 5/8
         r8
         c'4
         c'4
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr8\n\t\tc'4\n\t\tc'4\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedChunksWithRestFilledTokens_03( ):

   prefix_signal, prefix_denominator, prefix_lengths = [ ], 4, [0]
   suffix_signal, suffix_denominator, suffix_lengths = [ ], 4, [0]
   kaleid = SignalAffixedChunksWithRestFilledTokens(
      prefix_signal, prefix_denominator, prefix_lengths,
      suffix_signal, suffix_denominator, suffix_lengths)

   duration_tokens = [(5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         r2
         r8
      }
      {
         \time 5/8
         r2
         r8
      }
      {
         \time 5/8
         r2
         r8
      }
   }
   '''

   assert staff.format == '\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr8\n\t}\n}'
