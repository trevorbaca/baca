from abjad.tools import durtools
from abjad.tools import mathtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _RestMaker(_RhythmicKaleid):
   '''Big-endian rest maker.
   '''
   
   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      seeds = self._handle_none_seeds(seeds)
      rest_lists = self._make_rest_lists(duration_tokens)
      return rest_lists

   ## PRIVATE METHODS ##

   ## note currently used; maybe used later by subclasses of this class
   def _make_rest_numerator_tuples(self, duration_tokens):
      rest_numerators, rest_denominators = [ ], [ ]
      for duration_token in duration_tokens:
         duration_pair = durtools.duration_token_to_duration_pair(duration_token)
         duration_numerator = duration_pair[0]
         rest_numerator_tuple = mathtools.partition_integer_into_canonic_parts(
            duration_numerator, direction = 'big-endian')
         rest_denominators.append(duration_pair[1])
      return rest_numerators, rest_denominators
