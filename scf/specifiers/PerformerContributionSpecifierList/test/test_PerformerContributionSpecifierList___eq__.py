import baca


def test_PerformerContributionSpecifierList___eq___01():

    pcs_1 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = baca.scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    pcsl_1 = baca.scf.specifiers.PerformerContributionSpecifierList([pcs_1, pcs_2])
    pcsl_2 = baca.scf.specifiers.PerformerContributionSpecifierList([pcs_1, pcs_2])
    pcsl_3 = baca.scf.specifiers.PerformerContributionSpecifierList()

    assert pcsl_1 == pcsl_1
    assert pcsl_1 == pcsl_2
    assert not pcsl_1 == pcsl_3
    assert pcsl_2 == pcsl_1
    assert pcsl_2 == pcsl_2
    assert not pcsl_2 == pcsl_3
    assert not pcsl_3 == pcsl_1
    assert not pcsl_3 == pcsl_2
    assert pcsl_3 == pcsl_3
