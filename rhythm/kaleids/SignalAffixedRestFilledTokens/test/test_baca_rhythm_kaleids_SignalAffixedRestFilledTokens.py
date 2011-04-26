from abjad import *
from baca.rhythm.kaleids import *


def test_baca_rhythm_kaleids_SignalAffixedRestFilledTokens_01( ):

#   prefix_signal, prefix_denominator, prefix_lengths = [1], 4, [0, 1]
#   suffix_signal, suffix_denominator, suffix_lengths = [1], 32, [1]
#   kaleid = SignalAffixedRestFilledTokens(
#      prefix_signal, prefix_denominator, prefix_lengths,
#      suffix_signal, suffix_denominator, suffix_lengths)

   prefix_signal, prefix_lengths = [8], [0, 1]
   suffix_signal, suffix_lengths = [1], [1]
   denominator = 32
   kaleid = SignalAffixedRestFilledTokens(
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

   duration_tokens = [(5, 8), (5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         r2
         r16.
         c'32
      }
      {
         \time 5/8
         c'4
         r4
         r16.
         c'32
      }
      {
         \time 5/8
         r2
         r16.
         c'32
      }
      {
         \time 5/8
         c'4
         r4
         r16.
         c'32
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr16.\n\t\tc'32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tr4\n\t\tr16.\n\t\tc'32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr2\n\t\tr16.\n\t\tc'32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tr4\n\t\tr16.\n\t\tc'32\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedRestFilledTokens_02( ):

#   prefix_signal, prefix_denominator, prefix_lengths = [1], 4, [1, 2, 3, 4]
#   suffix_signal, suffix_denominator, suffix_lengths = [1], 32, [1]
#   kaleid = SignalAffixedRestFilledTokens(
#      prefix_signal, prefix_denominator, prefix_lengths,
#      suffix_signal, suffix_denominator, suffix_lengths)

   prefix_signal, prefix_lengths = [8], [1, 2, 3, 4]
   suffix_signal, suffix_lengths = [1], [1]
   denominator = 32
   kaleid = SignalAffixedRestFilledTokens(
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

   duration_tokens = [(5, 8), (5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         c'4
         r4
         r16.
         c'32
      }
      {
         \time 5/8
         c'4
         c'4
         r16.
         c'32
      }
      {
         \time 5/8
         c'4
         c'4
         c'8
      }
      {
         \time 5/8
         c'4
         c'4
         c'8
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tr4\n\t\tr16.\n\t\tc'32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tr16.\n\t\tc'32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'4\n\t\tc'4\n\t\tc'8\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedRestFilledTokens_03( ):

#   prefix_signal, prefix_denominator, prefix_lengths = [1], 32, [1]
#   suffix_signal, suffix_denominator, suffix_lengths = [1], 4, [1, 2, 3]
#   kaleid = SignalAffixedRestFilledTokens(
#      prefix_signal, prefix_denominator, prefix_lengths,
#      suffix_signal, suffix_denominator, suffix_lengths)

   prefix_signal, prefix_lengths = [1], [1]
   suffix_signal, suffix_lengths = [8], [1, 2, 3]
   denominator = 32
   kaleid = SignalAffixedRestFilledTokens(
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

   duration_tokens = [(5, 8), (5, 8), (5, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 5/8
         c'32
         r4
         r16.
         c'4
      }
      {
         \time 5/8
         c'32
         r16.
         c'4
         c'4
      }
      {
         \time 5/8
         c'32
         c'4
         c'4
         c'16.
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'32\n\t\tr4\n\t\tr16.\n\t\tc'4\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'32\n\t\tr16.\n\t\tc'4\n\t\tc'4\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'32\n\t\tc'4\n\t\tc'4\n\t\tc'16.\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedRestFilledTokens_04( ):

#   prefix_signal, prefix_denominator, prefix_lengths = [ ], 8, [0]
#   suffix_signal, suffix_denominator, suffix_lengths = [ ], 8, [0]
#   kaleid = SignalAffixedRestFilledTokens(
#      prefix_signal, prefix_denominator, prefix_lengths,
#      suffix_signal, suffix_denominator, suffix_lengths)

   prefix_signal, prefix_lengths = [ ], [0]
   suffix_signal, suffix_lengths = [ ], [0]
   denominator = 8
   kaleid = SignalAffixedRestFilledTokens(
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

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
