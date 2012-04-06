from abjad.tools import sequencetools
from abjad.tools import timetokentools
import baca
__all__ = []


pattern, denominator, prolation_addenda  = [1], 64, []
lefts, middles, rights = [-1], [0], [-1]
left_lengths, right_lengths = [1], [2]
sixty_fourths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
__all__.append('sixty_fourths')


pattern, denominator, prolation_addenda  = [1], 32, []
lefts, middles, rights = [-1], [0], [-1]
left_lengths, right_lengths = [1], [2]
thirty_seconds = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
__all__.append('thirty_seconds')
