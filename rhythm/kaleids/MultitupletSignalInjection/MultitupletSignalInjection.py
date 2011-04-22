from abjad.tools import durtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


class MultitupletSignalInjection(_RhythmicKaleid):
   '''Multituplet coruscation maker.
   '''

   def __init__(self, minimum_tuplet_duration, tuplet_counts, prolation_addenda, note_values,
      tuplet_counts_inspector, prolation_addenda_inspector, note_values_inspector):
      assert durtools.is_duration_token(minimum_tuplet_duration)
      assert seqtools.all_are_positive_integers(tuplet_counts)
      assert seqtools.all_are_integer_equivalent_numbers(prolation_addenda)
      assert seqtools.all_are_integer_equivalent_numbers(note_values)
      assert isinstance(tuplet_counts_inspector, types.FunctionType)
      assert isinstance(prolation_addenda_inspector, types.FunctionType)
      assert isinstance(note_values_inspector, types.FunctionType)
      self._minimum_tuplet_duration = durtools.duration_token_to_rational(minimum_tuplet_duration)
      self._tuplet_counts = seqtools.CyclicTuple(tuplet_counts)
      self._prolation_addenda = seqtools.CyclicTuple(prolation_addenda)
      self._note_values = seqtools.CyclicTuple(note_values)
      self._tuplet_counts_inspector = tuplet_counts_inspector
      self._prolation_addenda_inspector = prolation_addenda_inspector
      self._note_values_inspector = note_values_inspector

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      if seeds is None:
         seeds = [ ]
      duration_pairs = durtools.duration_tokens_to_duration_pairs(duration_tokens)
      tuplet_counts = self._tuplet_counts_inspector(duration_pairs, seeds)
      prolation_addenda = self._prolation_addenda_inspector(duration_pairs, seeds)
      note_values = self._note_values_inspector(duration_pairs, seeds)
      return duration_pairs
