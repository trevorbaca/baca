from abjad import *
from baca.rhythm.kaleids import *


def test_baca_rhythm_kaleids_SignalAffixedNoteFilledTokens_01( ):

   prefix_signal, prefix_lengths = [-8], [0, 1]
   suffix_signal, suffix_lengths = [-1], [1]
   denominator = 32
   kaleid = SignalAffixedNoteFilledTokens(
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
         c'2
         c'16.
         r32
      }
      {
         \time 5/8
         r4
         c'4
         c'16.
         r32
      }
      {
         \time 5/8
         c'2
         c'16.
         r32
      }
      {
         \time 5/8
         r4
         c'4
         c'16.
         r32
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'16.\n\t\tr32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tc'4\n\t\tc'16.\n\t\tr32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'16.\n\t\tr32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tc'4\n\t\tc'16.\n\t\tr32\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedNoteFilledTokens_02( ):

   prefix_signal, prefix_lengths = [-8], [1, 2, 3, 4]
   suffix_signal, suffix_lengths = [-1], [1]
   denominator = 32
   kaleid = SignalAffixedNoteFilledTokens(
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
         r4
         c'4
         c'16.
         r32
      }
      {
         \time 5/8
         r4
         r4
         c'16.
         r32
      }
      {
         \time 5/8
         r4
         r4
         r8
      }
      {
         \time 5/8
         r4
         r4
         r8
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tc'4\n\t\tc'16.\n\t\tr32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tr4\n\t\tc'16.\n\t\tr32\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tr4\n\t\tr8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr4\n\t\tr4\n\t\tr8\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedNoteFilledTokens_03( ):

   prefix_signal, prefix_lengths = [-1], [1]
   suffix_signal, suffix_lengths = [-8], [1, 2, 3]
   denominator = 32
   kaleid = SignalAffixedNoteFilledTokens(
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
         r32
         c'4
         c'16.
         r4
      }
      {
         \time 5/8
         r32
         c'16.
         r4
         r4
      }
      {
         \time 5/8
         r32
         r4
         r4
         r16.
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tr32\n\t\tc'4\n\t\tc'16.\n\t\tr4\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr32\n\t\tc'16.\n\t\tr4\n\t\tr4\n\t}\n\t{\n\t\t\\time 5/8\n\t\tr32\n\t\tr4\n\t\tr4\n\t\tr16.\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedNoteFilledTokens_04( ):

   prefix_signal, prefix_lengths = [ ], [0]
   suffix_signal, suffix_lengths = [ ], [0]
   denominator = 8
   kaleid = SignalAffixedNoteFilledTokens(
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
         c'2
         c'8
      }
      {
         \time 5/8
         c'2
         c'8
      }
      {
         \time 5/8
         c'2
         c'8
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'2\n\t\tc'8\n\t}\n}"


def test_baca_rhythm_kaleids_SignalAffixedNoteFilledTokens_05( ):

   prefix_signal, prefix_lengths = [-1], [1]
   suffix_signal, suffix_lengths = [-1], [1]
   denominator = 8
   prolation_addenda = [1, 0, 3]
   kaleid = SignalAffixedNoteFilledTokens(
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator,
      prolation_addenda = prolation_addenda)

   duration_tokens = [(4, 8), (4, 8), (4, 8)]
   leaf_lists = kaleid(duration_tokens)
   leaves = seqtools.flatten_sequence(leaf_lists)

   staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
   measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   r'''
   \new Staff {
      {
         \time 4/8
         \times 4/5 {
            r8
            c'4.
            r8
         }
      }
      {
         \time 4/8
         {
            r8
            c'4
            r8
         }
      }
      {
         \time 4/8
         \times 4/7 {
            r8
            c'2 ~
            c'8
            r8
         }
      }
   }
   '''

   assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/5 {\n\t\t\tr8\n\t\t\tc'4.\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\tr8\n\t\t\tc'4\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t\\times 4/7 {\n\t\t\tr8\n\t\t\tc'2 ~\n\t\t\tc'8\n\t\t\tr8\n\t\t}\n\t}\n}"
