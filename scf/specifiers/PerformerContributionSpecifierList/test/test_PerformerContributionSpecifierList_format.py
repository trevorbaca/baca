import baca


def test_PerformerContributionSpecifierList_format_01():

    pcs_1 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    pcsl = baca.scf.specifiers.PerformerContributionSpecifierList([pcs_1, pcs_2])

    '''
    PerformerContributionSpecifierList([
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
        ])
    '''

    assert pcsl.format == "PerformerContributionSpecifierList([\n\tPerformerContributionSpecifier(\n\t\tarticulation_specifier='foo',\n\t\tclef_specifier='bar',\n\t\tdirective_specifier=['apple', 'banana', 'cherry'],\n\t\t),\n\tPerformerContributionSpecifier(\n\t\tarticulation_specifier='blee',\n\t\tclef_specifier='blah',\n\t\tdirective_specifier=['durian'],\n\t\t),\n\t])"
