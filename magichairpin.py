from abjad.hairpin.spanners import _Hairpin

class _MagicHairpin(_Hairpin):

   def __init__(self, leaves):
      _Hairpin.__init__(self, leaves)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirst(leaf, ('Note', 'Chord')):
         result.append('\\%s' % self._shape)
      if self._isMyLast(leaf, ('Note', 'Chord')):
         if not leaf.dynamics.mark:
            result.append('\\!')
      return result
