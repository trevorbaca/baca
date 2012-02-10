import baca


def test_PerformerContributionSpecifier_format_01():

    specifier = baca.scf.PerformerContributionSpecifier()
    specifier.articulation_indicator = 'foo'
    specifier.clef_indicator = 'bar'
    specifier.directive_indicator = ['apple', 'banana', 'cherry']

    '''
    PerformerContributionSpecifier(
        articulation_indicator='foo',
        clef_indicator='bar',
        directive_indicator=['apple', 'banana', 'cherry'],
        )
    '''

    assert specifier.format == "PerformerContributionSpecifier(\n\tarticulation_indicator='foo',\n\tclef_indicator='bar',\n\tdirective_indicator=['apple', 'banana', 'cherry'],\n\t)"
