from abjad import *
import handlertools
import scf


def test_PatternedArticulationsHandlerEditor_run_01():

    editor = scf.editors.PatternedArticulationsHandlerEditor()
    editor.run(user_input="1 [['.', '^'], ['.']] (1, 16) (1, 8) cs'' c''' done", is_autoadvancing=True)


    handler = handlertools.articulations.PatternedArticulationsHandler(
        articulation_lists=[['.', '^'], ['.']],
        minimum_prolated_duration=Duration(1, 16),
        maximum_prolated_duration=Duration(1, 8),
        minimum_written_pitch=pitchtools.NamedChromaticPitch("cs''"),
        maximum_written_pitch=pitchtools.NamedChromaticPitch("c'''"))

    assert editor.target == handler
