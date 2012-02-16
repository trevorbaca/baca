import baca


def test_InteractiveEditor_target_attribute_tokens_01():

    editor = baca.scf.editors.MusicSpecifierEditor()
    assert editor.target_attribute_tokens == []
