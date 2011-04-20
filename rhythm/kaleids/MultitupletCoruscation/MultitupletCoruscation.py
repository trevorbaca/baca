from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


## TODO: rename to MultitupletSignalInjection
class MultitupletCoruscation(_RhythmicKaleid):
   '''Multituplet coruscation maker.
   '''

   def __init__(self, tuplet_counts, prolation_addenda, note_values,
      tuplet_counts_inspector, prolation_addenda_inspector, note_values_inspector):
      assert seqtools.all_are_positive_integers(tuplet_counts)
      assert seqtools.all_are_integer_equivalent_numbers(prolation_addenda)
      assert seqtools.all_are_integer_equivalent_numbers(note_values)
      assert isinstance(tuplet_counts_inspector, types.FunctionType)
      assert isinstance(prolation_addenda_inspector, types.FunctionType)
      assert isinstance(note_values_inspector, types.FunctionType)
      self._tuplet_counts = seqtools.CyclicTuple(tuplet_counts)
      self._prolation_addenda = seqtools.CyclicTuple(prolation_addenda)
      self._note_values = seqtools.CyclicTuple(note_values)
      self._tuplet_counts_inspector = tuplet_counts_inspector
      self._prolation_addenda_inspector = prolation_addenda_inspector
      self._note_values_inspector = note_values_inspector

   ## OVERLOADS ##

   def __call__(self, duration_pairs):
      '''Make rhythm from duration pairs.
      '''
      pass
