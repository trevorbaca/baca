from abjad.tools import mathtools
from abjad.tools import seqtools


class W(object):
   '''W-rhythm::

      abjad> baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
      W(3x22)
   '''

   def __init__(self, measure_numerators, talea, n_voices):
      self._measures = self._make_nested_measure_lists(measure_numerators, talea, n_voices)
      self._voices = self._make_nested_voice_lists( )

   ## OVERLOADS ##

   def __repr__(self):
      voices = self.voices
      n_voices = len(voices)
      n_measures = len(voices[0])
      return '%s(%sx%s)' % (self.__class__.__name__, n_voices, n_measures)

   ## PRIVATE METHODS ##

   def _make_nested_measure_lists(self, measure_numerators, talea, n_voices):
      assert all([mathtools.is_positive_integer(x) for x in measure_numerators])
      assert all([mathtools.is_positive_integer(x) for x in talea])
      assert mathtools.is_nonnegative_integer(n_voices)
      args = (n_voices * sum(measure_numerators), mathtools.weight(talea))
      lcm = mathtools.least_common_multiple(*args)
      part_measure_weights = [n_voices * [x] for x in measure_numerators]
      part_measure_weights = seqtools.flatten_sequence(part_measure_weights)
      all_measure_weights = seqtools.repeat_sequence_to_weight_exactly(part_measure_weights, lcm)
      all_measure_divisions = seqtools.repeat_sequence_to_weight_exactly(talea, lcm)
      args = (all_measure_weights, all_measure_divisions)
      all_measure_divisions = seqtools.split_sequence_once_by_weights_with_overhang(*args)
      all_measure_divisions = seqtools.flatten_sequence(all_measure_divisions)
      args = (all_measure_divisions, all_measure_weights)
      tmp = seqtools.partition_sequence_once_by_weights_exactly_with_overhang
      all_measure_divisions = tmp(all_measure_divisions, all_measure_weights)
      args = (all_measure_divisions, [n_voices])
      all_measure_divisions = seqtools.partition_sequence_cyclically_by_counts_with_overhang(*args)
      return all_measure_divisions

   def _make_nested_voice_lists(self):
      voices = [ ]
      measures = self.measures
      n_voices = len(measures[0])
      for voice_index in range(n_voices):
         voice = [measure[voice_index] for measure in measures]
         voices.append(voice)
      return voices

   ## PUBLIC ATTRIBUTES ##

   @property
   def measures(self):
      '''Read-only zero-indexed measures::

         abjad> W = baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
         abjad> W.measures[10]
         [[6, 4], [6, 3, 1], [2, 6, 2]]

      Return list of lists.
      '''
      return self._measures

   @property
   def voices(self):
      '''Read-only zero-indexed voices::

         abjad> W = baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
         abjad> W.voices[0][10]
         [6, 4]

      Return list of lists.
      '''
      return self._voices
