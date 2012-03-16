import scf


def test_MusicSpecifierEditor_public_attributes_01():
    '''Without target.
    '''

    editor = scf.editors.MusicSpecifierEditor()

    assert editor.breadcrumb == 'music specifier'
    assert not editor.has_target
    assert editor.target is None
    assert editor.target_attribute_tokens == [
        ('nm', 'music specifier name', 'None'), 
        ('tp', 'tempo', 'None'), 
        ('pc', 'performer contributions', 'None')]
    assert editor.target_name is None


def test_MusicSpecifierEditor_public_attributes_02():
    '''With target.
    '''

    pcs_1 = scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    ms = scf.specifiers.MusicSpecifier()
    ms.music_specifier_name = 'blue music'
    ms.tempo = 90
    ms.performer_contribution_specifiers.extend([pcs_1, pcs_2])

    r'''
    MusicSpecifier(
        music_specifier_name='blue music',
        performer_contribution_specifiers=PerformerContributionSpecifierInventory(
            PerformerContributionSpecifier(
                articulation_specifier='foo',
                clef_specifier='bar',
                directive_specifier=['apple', 'banana', 'cherry'],
                ),
            PerformerContributionSpecifier(
                articulation_specifier='blee',
                clef_specifier='blah',
                directive_specifier=['durian'],
                ),
            ),
        tempo=90,
        )
    '''

    editor = scf.editors.MusicSpecifierEditor(target=ms)

    assert editor.breadcrumb == 'blue music'
    assert editor.has_target
    assert editor.target is ms
    assert editor.target_attribute_tokens == [
        ('nm', 'music specifier name', 'blue music'), 
        ('tp', 'tempo', '90'), 
        ('pc', 'performer contributions', 'unknown performer, unknown performer')]
    assert editor.target_name == 'blue music'
