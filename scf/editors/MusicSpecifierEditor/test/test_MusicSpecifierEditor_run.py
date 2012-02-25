import baca


def test_MusicSpecifierEditor_run_01():

    editor = baca.scf.editors.MusicSpecifierEditor()
    editor.run(user_input='1 blue~music q')

    r'''
    MusicSpecifier(
        music_specifier_name='blue music',
        performer_contribution_specifiers=PerformerContributionSpecifierList([
            ]),
        )
    '''

    assert editor.target.format == "MusicSpecifier(\n\tmusic_specifier_name='blue music',\n\tperformer_contribution_specifiers=PerformerContributionSpecifierList([\n\t\t]),\n\t)"
