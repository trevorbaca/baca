from abjad import *
from abjad.tools import stafftools


def make_illustration_from_output_material(rhythm):

    staff = stafftools.RhythmicStaff(rhythm)
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)

    return illustration
