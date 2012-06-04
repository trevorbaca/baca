from abjad.tools import *
from helpers import *
from specification import ScoreSpecification
import baca.library as library


def test_solo_01():
    '''Single division interprets cyclically over single segment.
    Division truncates at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_02():
    '''Single division interprets cyclically over two segments.
    Division does not truncate at segment boundary.
    Division does truncate at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_03():
    '''Single division interprets cyclically over two segments.
    Division truncates at segment boundary because of truncate keyword.
    Division also truncates at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(3, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_04():
    '''Single division exacty equal to duration of single segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_05():
    '''Single division exactly equal to duration of single segment.
    Two such segments.
    Division does not truncate.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_07():
    '''Single division exactly equal to duration of single segment.
    Two such segments.
    Division truncates because truncate keyword is set to true.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(14, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_08():
    '''Single division greater in duration than single segment.
    Division truncates at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_09():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division does not truncate at segment boundary.
    Division does truncate at end of score.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)])
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name)

    assert score.format == read_test_output(__file__, current_function_name)


def test_solo_10():
    '''Single division greater in duration than single segment but lesser in duration than two segments.
    Division truncates at segment boundary because truncate keyword is set to true.
    Division replays from beginning of second segment.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    segment.set_divisions(segment.v1, [(20, 16)], truncate=True)
    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    write_test_output(score, __file__, current_function_name, go=True)

    assert score.format == read_test_output(__file__, current_function_name)
