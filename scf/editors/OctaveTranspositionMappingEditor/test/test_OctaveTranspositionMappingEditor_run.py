from abjad.tools import pitchtools
import scf


def test_OctaveTranspositionMappingEditor_run_01():

    editor = scf.editors.OctaveTranspositionMappingEditor()
    editor.run(user_input='add add source [A0, F#4] target 22 done add source (F#4, C8] target 26 done done done')

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, F#4]', 22), ('(F#4, C8]', 26)])
    assert editor.target == mapping
