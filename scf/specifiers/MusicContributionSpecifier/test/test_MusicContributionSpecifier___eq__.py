import scf


def test_MusicContributionSpecifier___eq___01():

    specifier_1 = scf.specifiers.MusicContributionSpecifier()
    specifier_1.articulation_specifier = 'foo'

    specifier_2 = scf.specifiers.MusicContributionSpecifier()
    specifier_2.articulation_specifier = 'foo'

    specifier_3 = scf.specifiers.MusicContributionSpecifier()
    specifier_3.articulation_specifier = 'foo'
    specifier_3.directive_specifier = ['apple', 'banana', 'cherry']

    assert specifier_1 == specifier_1
    assert specifier_1 == specifier_2
    assert not specifier_1 == specifier_3
    assert specifier_2 == specifier_1
    assert specifier_2 == specifier_2
    assert not specifier_2 == specifier_3
    assert not specifier_3 == specifier_1
    assert not specifier_3 == specifier_2
    assert specifier_3 == specifier_3
