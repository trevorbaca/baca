from abjad.tools import resttools
from baca.rhythm.kaleids._RestMaker import _RestMaker


class RestFilledTokens(_RestMaker):
   '''Rest-filled tokens.

   See the test file for examples.
   '''

   ## PRIVATE METHODS ##

   def _make_rest_lists(self, duration_tokens):
      rest_lists = [ ]
      for duration_token in duration_tokens:
         rest_list = resttools.make_rests([duration_token], direction = 'big-endian')
         rest_lists.append(rest_list)
      return rest_lists
