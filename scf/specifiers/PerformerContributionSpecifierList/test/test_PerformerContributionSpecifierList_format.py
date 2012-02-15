import baca


def test_PerformerContributionSpecifierList_format_01():

    pcs_1 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_indicator = 'foo'
    pcs_1.clef_indicator = 'bar'
    pcs_1.directive_indicator = ['apple', 'banana', 'cherry']

    pcs_2 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_indicator = 'blee'
    pcs_2.clef_indicator = 'blah'
    pcs_2.directive_indicator = ['durian']

    pcsl = baca.scf.specifiers.PerformerContributionSpecifierList([pcs_1, pcs_2])

    '''
    PerformerContributionSpecifierList(
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
        )
    '''

    assert pcsl.format == "PerformerContributionSpecifierList(\n\tPerformerContributionSpecifier(\n\t\tarticulation_indicator='foo',\n\t\tclef_indicator='bar',\n\t\tdirective_indicator=['apple', 'banana', 'cherry'],\n\t\t),\n\tPerformerContributionSpecifier(\n\t\tarticulation_indicator='blee',\n\t\tclef_indicator='blah',\n\t\tdirective_indicator=['durian'],\n\t\t),\n\t)"
