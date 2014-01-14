from abjad import *
import baca
__all__ = []


sixty_fourths = rhythmmakertools.TaleaRhythmMaker(
    talea=(1,), 
    talea_denominator=64, 
    burnish_output=True,
    beam_each_cell=True,
    )
sixty_fourths.beam = True
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)
