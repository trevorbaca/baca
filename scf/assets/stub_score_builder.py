from abjad import *
from output import data


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves()
lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
