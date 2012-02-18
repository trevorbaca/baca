import baca


def test_PackageWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    assert wrangler.has_toplevel_packages
    assert wrangler.has_wrangled_packages
    assert 'lidercfeny' in wrangler.score_package_short_names
    assert wrangler.toplevel_global_package_importable_name is None
    assert wrangler.toplevel_score_package_importable_name_body is None
    assert 'lidercfeny' in wrangler.toplevel_score_package_importable_names
    assert wrangler.wrangled_global_package_importable_names == []
    assert 'lidercfeny' in wrangler.wrangled_score_package_importable_names
