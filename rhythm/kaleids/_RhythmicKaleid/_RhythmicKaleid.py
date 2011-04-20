from abjad.tools import durtools


class _RhythmicKaleid(object):

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % (self.__class__.__name__)

   ## PRIVATE METHODS ##

   def _duration_tokens_to_duration_pairs(self, duration_tokens):
      return [durtools.duration_token_to_duration_pair(token) for token in duration_tokens]
