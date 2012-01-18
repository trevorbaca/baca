from abjad import *
from output import demo_material


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(demo_material)
lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
