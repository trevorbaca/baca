import scf


def test_MusicSpecifier___eq___01():

    pcs_1 = scf.specifiers.MusicContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = scf.specifiers.MusicContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    ms_1 = scf.specifiers.MusicSpecifier()
    ms_1.music_specifier_name = 'blue music'
    ms_1.tempo = 90
    ms_1.extend([pcs_1, pcs_2])

    pcs_3 = scf.specifiers.MusicContributionSpecifier()
    pcs_3.articulation_specifier = 'foo'
    pcs_3.clef_specifier = 'bar'
    pcs_3.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_4 = scf.specifiers.MusicContributionSpecifier()
    pcs_4.articulation_specifier = 'blee'
    pcs_4.clef_specifier = 'blah'
    pcs_4.directive_specifier = ['durian']

    ms_2 = scf.specifiers.MusicSpecifier()
    ms_2.music_specifier_name = 'blue music'
    ms_2.tempo = 90
    ms_2.extend([pcs_3, pcs_4])

    ms_3 = scf.specifiers.MusicSpecifier()

    assert ms_1 == ms_1
    assert ms_1 == ms_2
    assert not ms_1 == ms_3
    assert ms_2 == ms_1
    assert ms_2 == ms_2
    assert not ms_2 == ms_3
    assert not ms_3 == ms_1
    assert not ms_3 == ms_2
    assert ms_3 == ms_3
