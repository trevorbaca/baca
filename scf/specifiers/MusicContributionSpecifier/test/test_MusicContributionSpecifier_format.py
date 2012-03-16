import scf


def test_MusicContributionSpecifier_format_01():

    specifier = scf.specifiers.MusicContributionSpecifier()
    specifier.articulation_specifier = 'foo'
    specifier.clef_specifier = 'bar'
    specifier.directive_specifier = ['apple', 'banana', 'cherry']

    '''
    specifiers.MusicContributionSpecifier(
        articulation_specifier='foo',
        clef_specifier='bar',
        directive_specifier=['apple', 'banana', 'cherry']
        )
    '''

    assert specifier.format == "specifiers.MusicContributionSpecifier(\n\tarticulation_specifier='foo',\n\tclef_specifier='bar',\n\tdirective_specifier=['apple', 'banana', 'cherry']\n\t)"


def test_MusicContributionSpecifier_format_02():

    specifier = scf.specifiers.MusicContributionSpecifier()
    assert specifier.format == 'specifiers.MusicContributionSpecifier()'
