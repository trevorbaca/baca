from abjad import *
from output_material import illustration_builder


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(illustration_builder)
illustration = lilypondfiletools.make_basic_lilypond_file(score)