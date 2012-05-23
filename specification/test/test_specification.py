from abjad.tools import *
from specification import ScoreSpecification
import baca.library as library
import inspect
import os


render_pdfs = False
cache_pdfs = False

def manage_pdfs(segments, render_pdfs, cache_pdfs, test_function_name):
    if render_pdfs or cache_pdfs:
        total_segments = len(segments)
        for segment_number, segment in enumerate(segments, 1):
            lilypond_file = library.make_baca_letter_layout(segment)
            test_number = int(test_function_name.split('_')[-1])
            title = 'specification {} ({}/{})'.format(test_number, segment_number, total_segments)
            lilypond_file.header_block.title = markuptools.make_centered_title_markup(title, font_size=6)
            lilypond_file.layout_block.score.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
            if render_pdfs:
                iotools.show(lilypond_file)
            if cache_pdfs:
                parent_directory_name = os.path.dirname(__file__)
                file_name = '{}_{}.pdf'.format(test_function_name, segment_number)
                pdf_path_name = os.path.join(parent_directory_name, file_name)
                iotools.write_expr_to_pdf(lilypond_file, pdf_path_name)

def test_specification_01():
    '''Rhythm only.
    Create 4-staff score S in sections T1, T2.
    Set T1 time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set T1 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set T1 1 & 2 rhythm equal to token-burnished running 32nd notes.
    Set T1 3 & 4 divisions equal to T1 time signatures.
    Set T1 3 & 4 rhythm equal to note-filled tokens.

    Set T2 time signatures equal to the last 2 time signatures of T1.
    Let all other T1 specifications continue to T2.
    '''
    
    score = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))

    segment = score.append_segment(name='T1')
    segment.set_time_signatures(segment, [(3, 8), (3, 8), (2, 8), (2, 8)])

    violins = [segment.v1, segment.v2]
    segment.set_divisions(violins, [(3, 16)])
    segment.set_rhythm(violins, library.thirty_seconds)

    lower = [segment.v3, segment.v4]
    segment.set_rhythm(lower, library.note_filled_tokens)

    segment = score.append_segment(name='T2')
    segment.set_time_signatures(segment, score.retrieve('time_signatures', 'T1'), offset=-2, count=2)

    segments = score.notate()

    assert score['T1'].time_signatures == [(3, 8), (3, 8), (2, 8), (2, 8)]
    assert score['T2'].time_signatures == [(2, 8), (2, 8)]

    manage_pdfs(segments, render_pdfs, cache_pdfs, introspectiontools.get_current_function_name())
