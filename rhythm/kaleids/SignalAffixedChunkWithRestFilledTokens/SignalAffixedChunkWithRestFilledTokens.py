from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._SignalAffixedChunkWithFilledTokens import _SignalAffixedChunkWithFilledTokens


class SignalAffixedChunkWithRestFilledTokens(_SignalAffixedChunkWithFilledTokens):
   '''Signal-affixed chunks with rest-filled tokens.
   '''

   ## PRIVATE METHODS ##

   def _make_middle_of_numeric_map_part(self, middle):
      if 0 < middle:
         return (-abs(middle), )
      else:
         return ( )
