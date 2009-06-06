from abjad.tools import listtools
from abjad.tools import pitchtools


def constellate(psets, r):
   '''Return outer product of octave transpositions of psets in r.'''

   transpositions = [
      pitchtools.octave_transpositions(pset, r) for pset in psets]
   result = listtools.outer_product(transpositions)
   for i, part in enumerate(result):
      result[i] = listtools.flatten(part)
   [x.sort( ) for x in result]
   return result
