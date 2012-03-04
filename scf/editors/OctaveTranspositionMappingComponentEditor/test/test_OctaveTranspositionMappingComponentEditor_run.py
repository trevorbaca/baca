from abjad.tools import pitchtools
import scf


def test_OctaveTranspositionMappingComponentEditor_run_01():

    editor = scf.editors.OctaveTranspositionMappingComponentEditor()
    editor.run(user_input='source [A0, C8] target -18 q')
    
    assert editor.target == pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
