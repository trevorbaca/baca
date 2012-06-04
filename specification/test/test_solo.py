from abjad.tools import *
from helpers import *
from specification import ScoreSpecification
import baca.library as library


def test_solo_01():
    '''Single division will interpret in repetition over single segment.
    Division will truncate at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))

    segment = specification.append_segment('T1')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_02():
    '''Single division will interpret in repetition over two segments.
    Division will not truncate at segment boundary.
    Division will truncate at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))

    segment = specification.append_segment('T1')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment('T2')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_03():
    '''Single division will interpret in repetition over two segments.
    Division will truncate at segment boundary because of truncate keyword.
    Division will also truncate at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    
    segment = specification.append_segment('T1')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment('T2')

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)
