import scf


def test_InteractiveEditor_target_attribute_tokens_01():

    editor = scf.editors.MusicSpecifierEditor()
    assert editor.target_attribute_tokens == [
        ('nm', 'music specifier name', 'None'), 
        ('tp', 'tempo', 'None'), 
        ('pc', 'performer contributions', 'None')]
