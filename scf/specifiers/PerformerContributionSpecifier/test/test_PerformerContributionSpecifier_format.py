import scf


def test_PerformerContributionSpecifier_format_01():

    specifier = scf.specifiers.PerformerContributionSpecifier()
    specifier.articulation_specifier = 'foo'
    specifier.clef_specifier = 'bar'
    specifier.directive_specifier = ['apple', 'banana', 'cherry']

    '''
    specifiers.PerformerContributionSpecifier(
        articulation_specifier='foo',
        clef_specifier='bar',
        directive_specifier=['apple', 'banana', 'cherry'],
        )
    '''

    assert specifier.format == "specifiers.PerformerContributionSpecifier(\n\tarticulation_specifier='foo',\n\tclef_specifier='bar',\n\tdirective_specifier=['apple', 'banana', 'cherry'],\n\t)"
