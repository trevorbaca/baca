import scf


def test_PerformerContributionSpecifierInventory_format_01():

    pcs_1 = scf.specifiers.PerformerContributionSpecifier()
    pcs_1.articulation_specifier = 'foo'
    pcs_1.clef_specifier = 'bar'
    pcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    pcs_2 = scf.specifiers.PerformerContributionSpecifier()
    pcs_2.articulation_specifier = 'blee'
    pcs_2.clef_specifier = 'blah'
    pcs_2.directive_specifier = ['durian']

    pcsl = scf.specifiers.PerformerContributionSpecifierInventory([pcs_1, pcs_2])

    '''
    specifiers.PerformerContributionSpecifierInventory([
        specifiers.PerformerContributionSpecifier(
            articulation_specifier='foo',
            clef_specifier='bar',
            directive_specifier=['apple', 'banana', 'cherry'],
            ),
        specifiers.PerformerContributionSpecifier(
            articulation_specifier='blee',
            clef_specifier='blah',
            directive_specifier=['durian'],
            ),
        ])
    '''

    assert pcsl.format == "specifiers.PerformerContributionSpecifierInventory([\n\tspecifiers.PerformerContributionSpecifier(\n\t\tarticulation_specifier='foo',\n\t\tclef_specifier='bar',\n\t\tdirective_specifier=['apple', 'banana', 'cherry']\n\t\t),\n\tspecifiers.PerformerContributionSpecifier(\n\t\tarticulation_specifier='blee',\n\t\tclef_specifier='blah',\n\t\tdirective_specifier=['durian']\n\t\t)\n\t])"


def test_PerformerContributionSpecifierInventory_format_02():

    specifier_1 = scf.specifiers.PerformerContributionSpecifier()
    specifier_1.articulation_specifier = 'foo'
    specifier_1.clef_specifier = 'bar'
    specifier_1.directive_specifier = ['apple', 'banana', 'cherry']

    specifier_2 = scf.specifiers.PerformerContributionSpecifier()

    inventory = scf.specifiers.PerformerContributionSpecifierInventory()
    inventory.extend([specifier_1, specifier_2])

    r'''
    specifiers.PerformerContributionSpecifierInventory([
        specifiers.PerformerContributionSpecifier(
            articulation_specifier='foo',
            clef_specifier='bar',
            directive_specifier=['apple', 'banana', 'cherry']
            ),
        specifiers.PerformerContributionSpecifier()
        ])
    '''

    assert inventory._z == "specifiers.PerformerContributionSpecifierInventory([\n\tspecifiers.PerformerContributionSpecifier(\n\t\tarticulation_specifier='foo',\n\t\tclef_specifier='bar',\n\t\tdirective_specifier=['apple', 'banana', 'cherry']\n\t\t),\n\tspecifiers.PerformerContributionSpecifier()\n\t])"
