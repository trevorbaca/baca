import baca


def test_MusicSpecifier_01():

    pcs_1 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_indicator = 'foo'
    pcs_1.clef_indicator = 'bar'
    pcs_1.directive_indicator = ['apple', 'banana', 'cherry']

    pcs_2 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_indicator = 'blee'
    pcs_2.clef_indicator = 'blah'
    pcs_2.directive_indicator = ['durian']

    ms = baca.scf.specifiers.MusicSpecifier()
    ms.music_specifier_name = 'blue music'
    ms.tempo = 90
    ms.performer_contribution_specifiers.extend([pcs_1, pcs_2])


    '''
    MusicSpecifier(
        music_specifier_name='blue music',
        performer_contribution_specifiers=PerformerContributionSpecifierList(
            PerformerContributionSpecifier(
                articulation_indicator='foo',
                clef_indicator='bar',
                directive_indicator=['apple', 'banana', 'cherry'],
                ),
            PerformerContributionSpecifier(
                articulation_indicator='blee',
                clef_indicator='blah',
                directive_indicator=['durian'],
                ),
            ),
        tempo=90,
        )
    '''

    "MusicSpecifier(\n\tmusic_specifier_name='blue music',\n\tperformer_contribution_specifiers=PerformerContributionSpecifierList(\n\t\tPerformerContributionSpecifier(\n\t\t\tarticulation_indicator='foo',\n\t\t\tclef_indicator='bar',\n\t\t\tdirective_indicator=['apple', 'banana', 'cherry'],\n\t\t\t),\n\t\tPerformerContributionSpecifier(\n\t\t\tarticulation_indicator='blee',\n\t\t\tclef_indicator='blah',\n\t\t\tdirective_indicator=['durian'],\n\t\t\t),\n\t\t),\n\ttempo=90,\n\t)"
