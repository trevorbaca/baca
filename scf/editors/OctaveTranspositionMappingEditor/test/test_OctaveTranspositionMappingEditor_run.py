from abjad.tools import pitchtools
import scf


def test_OctaveTranspositionMappingEditor_run_01():

    editor = scf.editors.OctaveTranspositionMappingEditor()
    editor.run(user_input='add source [A0, C4) target -18 done add source [C4, C8] target -15 done q')

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', -18), ('[C4, C8]', -15)])
    assert editor.target == mapping
