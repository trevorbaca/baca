from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools
import baca
__all__ = []



pattern, denominator, prolation_addenda  = [1], 64, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [1], [2]
sixty_fourths = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
    pattern, denominator, prolation_addenda,
    lefts, middles, rights,
    left_lengths, right_lengths)
sixty_fourths.beam = True
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)
