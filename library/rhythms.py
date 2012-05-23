from abjad.tools import sequencetools
from abjad.tools import timetokentools
import baca
__all__ = []



note_filled_tokens = timetokentools.NoteFilledTimeTokenMaker()
note_filled_tokens.name = 'note_filled_tokens'
__all__.append(note_filled_tokens.name)


rest_filled_tokens = timetokentools.RestFilledTimeTokenMaker()
rest_filled_tokens.name = 'rest_filled_tokens'
__all__.append(rest_filled_tokens.name)


pattern, denominator, prolation_addenda  = [1], 64, []
lefts, middles, rights = [-1], [0], [-1]
left_lengths, right_lengths = [1], [2]
sixty_fourths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)


pattern, denominator, prolation_addenda  = [1], 32, []
#lefts, middles, rights = [-1], [0], [-1]
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [1], [2]
thirty_seconds = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
thirty_seconds.beam = True
thirty_seconds.name = 'thirty_seconds'
__all__.append(thirty_seconds.name)
