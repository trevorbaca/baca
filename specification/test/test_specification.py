from abjad.tools import *
from specification import ScoreSpecification
import baca.library as library
import inspect
import os


def manage_output(score, test_function_name, render_pdf=False, cache_pdf=False, cache_ly=False):
    if not any([render_pdf, cache_pdf, cache_ly]):
        return
    lilypond_file = library.apply_baca_letter_layout(score)
    test_number = int(test_function_name.split('_')[-1])
    title = 'specification {}'.format(test_number)
    lilypond_file.header_block.title = markuptools.make_centered_title_markup(title, font_size=6)
    lilypond_file.layout_block.score.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
    parent_directory_name = os.path.dirname(__file__)
    if render_pdf:
        iotools.show(lilypond_file)
    if cache_pdf:
        file_name = '{}.pdf'.format(test_function_name)
        pdf_path_name = os.path.join(parent_directory_name, file_name)
        iotools.write_expr_to_pdf(lilypond_file, pdf_path_name)
    if cache_ly:
        file_name = '{}.ly'.format(test_function_name)
        ly_path_name = os.path.join(parent_directory_name, file_name)
        file(ly_path_name, 'w').write(score.format)

def read_score_ly_file(current_function_name):
    segment_ly_file_name = '{}.ly'.format(current_function_name)
    directory_name = os.path.dirname(__file__)
    segment_ly_path_name = os.path.join(directory_name, segment_ly_file_name)
    return file(segment_ly_path_name, 'r').read()


def test_specification_01():
    '''Rhythm only.
    Create 4-staff score S with sections T1, T2.
    Set T1 time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set T1 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set T1 1 & 2 rhythm equal to running 32nd notes.
    Set T1 3 & 4 divisions equal to T1 time signatures.
    Set T1 3 & 4 rhythm equal to note-filled tokens.

    Set T2 time signatures equal to the last 2 time signatures of T1.
    Let all other T1 specifications continue to T2.

    Tests for spanning divisions in 1 & 2 over T1 / T2.
    Tests for truncated divisions in 1 & 2 at the end of T2.
    '''
    
    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))

    segment = specification.append_segment(name='T1')
    segment.set_time_signatures(segment, [(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions(upper, [(3, 16)])
    segment.set_rhythm(upper, library.thirty_seconds)

    lower = [segment.v3, segment.v4]
    segment.set_rhythm(lower, library.note_filled_tokens)

    segment = specification.append_segment(name='T2')
    segment.set_time_signatures(segment, specification.retrieve('time_signatures', 'T1'), offset=-2, count=2)

    score = specification.interpret()

    assert specification['T1'].time_signatures == [(3, 8), (3, 8), (2, 8), (2, 8)]
    assert specification['T2'].time_signatures == [(2, 8), (2, 8)]

    current_function_name = introspectiontools.get_current_function_name()
    manage_output(score, current_function_name)

    assert score.format == read_score_ly_file(current_function_name)


def test_specification_02():
    '''As above with different divisions.
    
    Tests for spanning divisions in 1 & 2 and also in 3 & 4.
    '''
    
    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))

    segment = specification.append_segment(name='T1')
    segment.set_time_signatures(segment, [(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions(upper, [(5, 16)])
    segment.set_rhythm(upper, library.thirty_seconds)

    lower = [segment.v3, segment.v4]
    segment.set_divisions(lower, [(4, 16), (3, 16)])
    segment.set_rhythm(lower, library.note_filled_tokens)

    segment = specification.append_segment(name='T2')
    segment.set_time_signatures(segment, specification.retrieve('time_signatures', 'T1'), offset=-2, count=2)

    score = specification.interpret()

    assert specification['T1'].time_signatures == [(3, 8), (3, 8), (2, 8), (2, 8)]
    assert specification['T2'].time_signatures == [(2, 8), (2, 8)]

    current_function_name = introspectiontools.get_current_function_name()
    manage_output(score, current_function_name)

    assert score.format == read_score_ly_file(current_function_name)
