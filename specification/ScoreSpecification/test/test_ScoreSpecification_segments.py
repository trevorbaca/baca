from abjad.tools import *
from baca.specification.ScoreSpecification import ScoreSpecification


def test_ScoreSpecification_segments_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    
    assert not specification.segments


def test_ScoreSpecification_segments_02():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))

    specification.append_segment('1') 
    assert len(specification.segments) == 1

    specification.append_segment('2')
    assert len(specification.segments) == 2

    specification.segments.pop()
    assert len(specification.segments) == 1
