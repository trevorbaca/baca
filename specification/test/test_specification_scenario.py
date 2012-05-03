from abjad.tools import scoretemplatetools
from specification import ScoreSpecification
import baca.library as library
import py


def test_specification_scenario_01():
    '''Rhythm only.
    Create string quartet score S in sections T1, T2.
    Set T1 time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set T1 violins 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set T1 violins rhythm equal to token-burnished running 32nd notes.
    Set T1 viola & cello divisions equal to T1 time signatures.
    Set T1 violin & cello rhythm equal to note-filled tokens.

    Set T2 time signatures equal to the last 2 time signatures of T1.
    Let all other T1 specifications continue to T2.
    '''
    py.test.skip()
    
    score = ScoreSpecification(scoretemplatetools.StringQuartetScoreTemplate())

    segment = score.append_segment(name='T1') 
    segment.set_time_signatures(segment, [(3, 8), (3, 8), (2, 8), (2, 8)])

    violins = [segment.vn1, segment.vn2]
    segment.set_divisions(violins, [(3, 16)])
    segment.set_rhythm(violins, library.thirty_seconds)

    lower = [segment.va, segment.vc]
    segment.set_rhythm(lower, library.note_filled_tokens)

    segment = score.append_segment(name='T2')
    segment.set_time_signatures(segment, score.retrieve('T1', 'time_signatures'), offset=-2, count=2)

    score.interpret()
