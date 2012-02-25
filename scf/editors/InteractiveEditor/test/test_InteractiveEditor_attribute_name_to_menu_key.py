import scf


def test_InteractiveEditor_attribute_name_to_menu_key_01():

    editor = scf.editors.InteractiveEditor()
    menu_keys = []
    assert editor.attribute_name_to_menu_key('foo_bar_blah', menu_keys) == 'fbb'
