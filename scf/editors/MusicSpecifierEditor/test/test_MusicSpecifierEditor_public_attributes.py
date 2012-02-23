import baca


def test_MusicSpecifierEditor_public_attributes_01():

    editor = baca.scf.editors.MusicSpecifierEditor()

    assert editor.breadcrumb == 'music specifier editor'
    assert editor.target is None
    assert editor.target_attribute_tokens == [] 
    assert editor.target_name is None
