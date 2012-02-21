import baca

studio = baca.scf.studio.Studio()
wrangler = studio.score_package_wrangler


def test_ScorePackageWrangler_iteration_01():

    assert 'archipel' in wrangler.list_score_internal_wrangled_asset_importable_names()
    assert 'archipel' not in wrangler.list_score_internal_wrangled_asset_importable_names(head='aracilik')
    assert wrangler.list_score_internal_wrangled_asset_importable_names(head='asdf') == []


def test_ScorePackageWrangler_iteration_02():

    assert 'archipel' in wrangler.list_score_internal_asset_container_importable_names()
    assert 'archipel' not in wrangler.list_score_internal_asset_container_importable_names(head='aracilik')
    assert wrangler.list_score_internal_asset_container_importable_names(head='asdf') == []
    

def test_ScorePackageWrangler_iteration_03():

    assert 'archipel' in wrangler.list_visible_asset_short_names()
    assert 'archipel' not in wrangler.list_visible_asset_short_names(head='aracilik')
    assert wrangler.list_visible_asset_short_names(head='asdf') == []


def test_ScorePackageWrangler_iteration_04():

    assert 'archipel' in wrangler.list_wrangled_package_short_names()
    assert 'archipel' not in wrangler.list_wrangled_package_short_names(head='aracilik')
    assert wrangler.list_wrangled_package_short_names(head='asdf') == []
