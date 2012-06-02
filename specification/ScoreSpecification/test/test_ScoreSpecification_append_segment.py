from abjad.tools import *
from baca.specification.ScoreSpecification import ScoreSpecification


def test_ScoreSpecification_append_segment_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    assert segment.name == '1'
    assert len(specification.segments) == 1
    
    segment = specification.append_segment(name='foo')
    assert segment.name == 'foo'
    assert len(specification.segments) == 2
