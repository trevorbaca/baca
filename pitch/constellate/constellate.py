from abjad.chord import Chord
from abjad.note import Note
from abjad.tools import listtools
from abjad.tools import pitchtools


def constellate(pitch_number_lists, pitch_range, flatten = True):
   '''Return outer product of octave transpositions of 
   `pitch_number_lists` in `pitch_range`.'''

   if not isinstance(pitch_range, pitchtools.PitchRange):
      raise TypeError('must be pitch range.')

   transposition_list = [ ]
   for pnl in pitch_number_lists:
      transpositions = pitchtools.octave_transpositions(pnl, pitch_range)
      transposition_list.append(transpositions)

   result = listtools.outer_product(transposition_list)

   for pnl in result:
      if flatten:
         for i, part in enumerate(result):
            result[i] = listtools.flatten(part)
   
   for pnl in result:
      pnl.sort( )

   return result
