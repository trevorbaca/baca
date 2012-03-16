import scf


def test_MusicSpecifierEditor_run_01():

    editor = scf.editors.MusicSpecifierEditor()
    editor.run(user_input='1 blue~music q')

    r'''
    specifiers.MusicSpecifier(
        music_specifier_name='blue music',
        performer_contribution_specifiers=specifiers.PerformerContributionSpecifierInventory([
            ]),
        )
    '''

    assert editor.target.format == "specifiers.MusicSpecifier(\n\tmusic_specifier_name='blue music',\n\tperformer_contribution_specifiers=specifiers.PerformerContributionSpecifierInventory([])\n\t)"
