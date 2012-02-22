import baca


def test_PackageWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    assert wrangler.score_external_asset_container_importable_name is None
    assert wrangler.score_internal_asset_container_importable_name_infix is None
    assert 'lidercfeny' in \
        wrangler.list_score_internal_asset_container_importable_names()
    assert wrangler.list_score_external_asset_importable_names() == []
    assert 'lidercfeny' in wrangler.list_score_internal_asset_importable_names()
