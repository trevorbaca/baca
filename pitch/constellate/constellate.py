from abjad.chord import Chord
from abjad.note import Note
from abjad.tools import listtools
from abjad.tools import pitchtools


def constellate(psets, pitch_range):
   '''Return outer product of octave transpositions of `psets` in 
    `pitch_range`.'''

   if not all([
      isinstance(x, (Note, Chord, pitchtools.PitchSet)) for x in psets]):
      raise TypeError('must be note, chord or pitch set.')

   if not isinstance(pitch_range, pitchtools.PitchRange):
      raise TypeError('must be pitch range.')

   transpositions = [
      pitchtools.octave_transpositions(pset, pitch_range) for pset in psets]

   result = listtools.outer_product(transpositions)

   #for i, part in enumerate(result):
   #   result[i] = listtools.flatten(part)
   result = [reduce(Chord.__or__, partition) for partition in result]

   #[x.sort( ) for x in result]

   return result
