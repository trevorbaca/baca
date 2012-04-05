from baca.specification.ScoreSpecification import ScoreSpecification
from library import *
import baca
import py
import scf


def test_ScoreSpecification_interpret_segments_01():
    py.test.skip('finish')

    score_template = scf.templates.StringQuartetScoreTemplate
    score = ScoreSpecification(score_template)

    context_name_abbreviations = {}
    context_name_abbreviations['vn1'] = 'First Violin Voice'
    context_name_abbreviations['vn2'] = 'Second Violin Voice'
    context_name_abbreviations['va'] = 'Viola Voice'
    context_name_abbreviations['vc'] = 'Cello Voice'
    score.context_name_abbreviations = context_name_abbreviations
    score.initialize_context_name_abbreviations()

    segment = score.append_segment(name='A')
    segment.set_tempo(segment, 108)
    segment.set_time_signatures(segment, [(2, 8), (2, 8), (3, 8), (2, 8), (3, 8)])
    segment.set_aggregate(segment, baca.pitch.CC[0][0])
    segment.set_pitch_classes_timewise(segment, [0, 8, 9, 11, 1, 2, 4, 6, 3, 5, 7, 10])
    segment.set_rhythm(segment.vn1, (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_register(segment.vn1, cello_treble)
    segment.set_dynamics(segment.vn1, terraced_fortissimo)
    segment.set_rhythm(segment.vn2, (repeated_quarter_divisions_right, thirty_seconds))
    segment.set_register(segment.vn2, cello_treble)
    segment.set_dynamics(segment.vn2, terraced_fortissimo)
