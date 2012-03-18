import scf


def test_MusicSpecifier_format_01():
    '''Empty. No keywords.
    '''

    specifier = scf.specifiers.MusicSpecifier([])

    assert repr(specifier) == 'MusicSpecifier([])'
    assert specifier._storage_format == 'specifiers.MusicSpecifier([])'


def test_MusicSpecifier_format_02():
    '''Empty. With keywords.
    '''

    specifier = scf.specifiers.MusicSpecifier([], inventory_name='foo')

    assert repr(specifier) == "MusicSpecifier([], inventory_name='foo')"
    assert specifier._storage_format == "specifiers.MusicSpecifier([],\n\tinventory_name='foo'\n\t)"

    
def test_MusicSpecifier_format_03():
    '''Populated. Without keywords.
    '''

    pcs_1 = scf.specifiers.MusicContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = scf.specifiers.MusicContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    ms = scf.specifiers.MusicSpecifier()
    ms.extend([pcs_1, pcs_2])

    '''
    specifiers.MusicSpecifier(
        performer_contribution_specifiers=specifiers.MusicContributionSpecifierInventory([
            specifiers.MusicContributionSpecifier(
                articulation_specifier='foo',
                clef_specifier='bar',
                directive_specifier=['apple', 'banana', 'cherry']
                ),
            specifiers.MusicContributionSpecifier(
                articulation_specifier='blee',
                clef_specifier='blah',
                directive_specifier=['durian']
                )
            ])
        )
    '''

    assert ms.format == "specifiers.MusicSpecifier([\n\tspecifiers.MusicContributionSpecifier(\n\t\tarticulation_specifier='foo',\n\t\tclef_specifier='bar',\n\t\tdirective_specifier=['apple', 'banana', 'cherry']\n\t\t),\n\tspecifiers.MusicContributionSpecifier(\n\t\tarticulation_specifier='blee',\n\t\tclef_specifier='blah',\n\t\tdirective_specifier=['durian']\n\t\t)\n\t])"


def test_MusicSpecifier_format_04():
    '''Populated. With keywords.
    '''

    pcs_1 = scf.specifiers.MusicContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = scf.specifiers.MusicContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    ms = scf.specifiers.MusicSpecifier()
    ms.extend([pcs_1, pcs_2])

    ms.name = 'blue music'

    '''
    specifiers.MusicSpecifier(
        performer_contribution_specifiers=specifiers.MusicContributionSpecifierInventory([
            specifiers.MusicContributionSpecifier(
                articulation_specifier='foo',
                clef_specifier='bar',
                directive_specifier=['apple', 'banana', 'cherry']
                ),
            specifiers.MusicContributionSpecifier(
                articulation_specifier='blee',
                clef_specifier='blah',
                directive_specifier=['durian']
                )
            ],
            name='blue music'
        )
    '''
    
    assert repr(ms) == "MusicSpecifier([MusicContributionSpecifier(articulation_specifier='foo', clef_specifier='bar', directive_specifier=['apple', 'banana', 'cherry']), MusicContributionSpecifier(articulation_specifier='blee', clef_specifier='blah', directive_specifier=['durian'])], name='blue music')"

    assert ms._storage_format == "specifiers.MusicSpecifier([\n\tspecifiers.MusicContributionSpecifier(\n\t\tarticulation_specifier='foo',\n\t\tclef_specifier='bar',\n\t\tdirective_specifier=['apple', 'banana', 'cherry']\n\t\t),\n\tspecifiers.MusicContributionSpecifier(\n\t\tarticulation_specifier='blee',\n\t\tclef_specifier='blah',\n\t\tdirective_specifier=['durian']\n\t\t)\n\t],\n\tname='blue music'\n\t)"
