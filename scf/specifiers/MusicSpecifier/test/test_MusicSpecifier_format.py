import baca


def test_MusicSpecifier_format_01():

    pcs_1 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    ms = baca.scf.specifiers.MusicSpecifier()
    ms.music_specifier_name = 'blue music'
    ms.tempo = 90
    ms.performer_contribution_specifiers.extend([pcs_1, pcs_2])


    '''
    MusicSpecifier(
        music_specifier_name='blue music',
        performer_contribution_specifiers=PerformerContributionSpecifierList(
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

    "MusicSpecifier(\n\tmusic_specifier_name='blue music',\n\tperformer_contribution_specifiers=PerformerContributionSpecifierList(\n\t\tPerformerContributionSpecifier(\n\t\t\tarticulation_specifier='foo',\n\t\t\tclef_specifier='bar',\n\t\t\tdirective_specifier=['apple', 'banana', 'cherry'],\n\t\t\t),\n\t\tPerformerContributionSpecifier(\n\t\t\tarticulation_specifier='blee',\n\t\t\tclef_specifier='blah',\n\t\t\tdirective_specifier=['durian'],\n\t\t\t),\n\t\t),\n\ttempo=90,\n\t)"
