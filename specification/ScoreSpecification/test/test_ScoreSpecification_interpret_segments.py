from baca.specification.ScoreSpecification import ScoreSpecification
from library import *
import baca
import scf


# TODO: finish test
def test_ScoreSpecification_interpret_segments_01():

    specification = ScoreSpecification()
    specification.default_score_template = scf.templates.StringQuartetScoreTemplate()

    segment = specification.append_segment(name='A')
    segment.set_segment_tempo(108)
    segment.set_segment_time_signatures([(2, 8), (2, 8), (3, 8), (2, 8), (3, 8)])
    segment.set_segment_aggregate(baca.pitch.CC[0][0])
    segment.set_segment_pitch_classes_timewise([0, 8, 9, 11, 1, 2, 4, 6, 3, 5, 7, 10])
    segment.set_voice_rhythm('first violin', (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_voice_register('first violin', cello_treble)
    segment.set_voice_dynamics('first violin', terraced_fortissimo)
    segment.set_voice_rhythm('second violin', (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_voice_register('second violin', cello_treble)
    segment.set_voice_dynamics('second violin', terraced_fortissimo)
