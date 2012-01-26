from abjad import *
from output_material import demo_material


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(demo_material)
illustration = lilypondfiletools.make_basic_lilypond_file(score)
