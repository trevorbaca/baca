import scf


def test_MusicSpecifierEditor_run_01():

    editor = scf.editors.MusicSpecifierEditor()
    editor.run(user_input='name blue~music q')

    r'''
    specifiers.MusicSpecifier(
        inventory_name='blue music',
        performer_contribution_specifiers=specifiers.MusicContributionSpecifierInventory([
            ]),
        )
    '''

    assert editor.target.format == "specifiers.MusicSpecifier([],\n\tinventory_name='blue music'\n\t)"
