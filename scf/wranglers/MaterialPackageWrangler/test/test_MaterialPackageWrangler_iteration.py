import baca

studio = baca.scf.studio.Studio()
wrangler = studio.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_iteration_01():

    assert 'manos.mus.materials.aggregates' in \
        wrangler.list_score_internal_wrangled_package_importable_names()
    assert 'manos.mus.materials.aggregates' not in \
        wrangler.list_score_internal_wrangled_package_importable_names(head='aracilik')
    assert wrangler.list_score_internal_wrangled_package_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_02():

    assert 'manos.mus.materials' in \
        wrangler.list_score_internal_wrangler_target_package_importable_names()
    assert 'manos.mus.materials' not in \
        wrangler.list_score_internal_wrangler_target_package_importable_names(head='aracilik')
    assert wrangler.list_score_internal_wrangler_target_package_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_03():

    assert 'turquoise_pcs' in wrangler.list_visible_wrangled_package_short_names()
    assert 'turquoise_pcs' not in wrangler.list_visible_wrangled_package_short_names(head='aracilik')
    assert wrangler.list_visible_wrangled_package_short_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_04():

    assert 'baca.materials.red_sargasso' in \
        wrangler.list_wrangled_package_importable_names()
    assert 'manos.mus.materials.turquoise_pcs' in \
        wrangler.list_wrangled_package_importable_names()
    assert 'baca.materials.red_sargasso' not in \
        wrangler.list_wrangled_package_importable_names(head='aracilik')
    assert 'manos.mus.materials.turquoise_pcs' not in \
        wrangler.list_wrangled_package_importable_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_05():

    assert ('baca.materials.red_sargasso', 'red sargasso') in \
        wrangler.list_wrangled_package_menuing_pairs()
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') in \
        wrangler.list_wrangled_package_menuing_pairs()
    assert ('baca.materials.red_sargasso', 'red sargasso') not in \
        wrangler.list_wrangled_package_menuing_pairs(head='aracilik')
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') not in \
        wrangler.list_wrangled_package_menuing_pairs(head='aracilik')


def test_MaterialPackageWrangler_iteration_06():

    assert 'red_sargasso' in wrangler.list_wrangled_package_short_names()
    assert 'turquoise_pcs' in wrangler.list_wrangled_package_short_names()
    assert 'red_sargasso' not in wrangler.list_wrangled_package_short_names(head='aracilik')
    assert 'turquoise_pcs' not in wrangler.list_wrangled_package_short_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_07():

    assert 'red sargasso' in wrangler.list_wrangled_package_spaced_names()
    assert 'turquoise pcs' in wrangler.list_wrangled_package_spaced_names()
    assert 'red sargasso' not in wrangler.list_wrangled_package_spaced_names(head='aracilik')
    assert 'turquoise pcs' not in wrangler.list_wrangled_package_spaced_names(head='aracilik')
