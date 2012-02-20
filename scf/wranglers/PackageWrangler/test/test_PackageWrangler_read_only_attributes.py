import baca


def test_PackageWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    assert wrangler.score_external_wrangler_target_package_importable_name is None
    assert wrangler.score_internal_wrangler_target_package_importable_name_suffix is None
    assert 'lidercfeny' in \
        wrangler.list_score_internal_wrangler_target_package_importable_names()
    assert wrangler.score_external_wrangled_package_importable_names == []
    assert 'lidercfeny' in wrangler.list_score_internal_wrangled_package_importable_names()
