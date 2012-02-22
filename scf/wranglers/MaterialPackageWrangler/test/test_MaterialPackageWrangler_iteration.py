import baca

studio = baca.scf.studio.Studio()
wrangler = studio.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_iteration_01():
    '''Assets (all).
    '''

    assert 'red sargasso' in wrangler.list_asset_human_readable_names()
    assert 'turquoise pcs' in wrangler.list_asset_human_readable_names()
    assert 'red sargasso' not in wrangler.list_asset_human_readable_names(head='aracilik')
    assert 'turquoise pcs' not in wrangler.list_asset_human_readable_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_02():

    assert 'baca.materials.red_sargasso' in \
        wrangler.list_asset_importable_names()
    assert 'manos.mus.materials.turquoise_pcs' in \
        wrangler.list_asset_importable_names()
    assert 'baca.materials.red_sargasso' not in \
        wrangler.list_asset_importable_names(head='aracilik')
    assert 'manos.mus.materials.turquoise_pcs' not in \
        wrangler.list_asset_importable_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_03():

    assert '/Users/trevorbaca/Documents/other/baca/materials/red_notes' in \
        wrangler.list_asset_path_names()
    assert '/Users/trevorbaca/Documents/other/baca/materials/red_notes' not in \
        wrangler.list_asset_path_names(head='aracilik')
    assert wrangler.list_asset_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration004():
    
    # wrangler.list_asset_proxies()
    pass


def test_MaterialPackageWrangler_iteration_05():

    assert 'red_sargasso' in wrangler.list_asset_short_names()
    assert 'turquoise_pcs' in wrangler.list_asset_short_names()
    assert 'red_sargasso' not in wrangler.list_asset_short_names(head='aracilik')
    assert 'turquoise_pcs' not in wrangler.list_asset_short_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_06():
    '''Score-internal asset containers.
    '''

    assert 'manos.mus.materials' in \
        wrangler.list_score_internal_asset_container_importable_names()
    assert 'manos.mus.materials' not in \
        wrangler.list_score_internal_asset_container_importable_names(head='aracilik')
    assert wrangler.list_score_internal_asset_container_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_07():

    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials' in \
        wrangler.list_score_internal_asset_container_path_names()
    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials' not in \
        wrangler.list_score_internal_asset_container_path_names(head='aracilik')
    assert wrangler.list_score_internal_asset_container_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_08():
    '''Score-internal assets.
    '''

    assert 'manos.mus.materials.aggregates' in \
        wrangler.list_score_internal_asset_importable_names()
    assert 'manos.mus.materials.aggregates' not in \
        wrangler.list_score_internal_asset_importable_names(head='aracilik')
    assert wrangler.list_score_internal_asset_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_09():

    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials/aggregates' in \
        wrangler.list_score_internal_asset_path_names()
    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials/aggregates' not in \
        wrangler.list_score_internal_asset_path_names(head='aracilik')
    assert wrangler.list_score_internal_asset_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_10():
    '''Visible assets.
    '''

    assert 'turquoise pcs' in wrangler.list_visible_asset_human_readable_names()
    assert 'turquoise pcs' not in wrangler.list_visible_asset_human_readable_names(head='aracilik')
    assert wrangler.list_visible_asset_human_readable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_11():

   assert 'manos.mus.materials.turquoise_pcs' in \
        wrangler.list_visible_asset_importable_names()
   assert 'manos.mus.materials.turquoise_pcs' not in \
        wrangler.list_visible_asset_importable_names(head='aracilik')
   assert wrangler.list_visible_asset_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_12():

    assert ('baca.materials.red_sargasso', 'red sargasso') in \
        wrangler.list_visible_asset_menuing_pairs()
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') in \
        wrangler.list_visible_asset_menuing_pairs()
    assert ('baca.materials.red_sargasso', 'red sargasso') not in \
        wrangler.list_visible_asset_menuing_pairs(head='aracilik')
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') not in \
        wrangler.list_visible_asset_menuing_pairs(head='aracilik')


def test_MaterialPackageWrangler_iteration_13():

    # wrangler.list_visible_asset_proxies()
    pass
