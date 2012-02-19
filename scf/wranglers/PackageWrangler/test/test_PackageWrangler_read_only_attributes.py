import baca


def test_PackageWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    assert wrangler.has_toplevel_packages
    assert wrangler.has_wrangled_packages
    assert wrangler.toplevel_wrangler_target_package_importable_name is None
    assert wrangler.wrangled_score_package_importable_name_prefix is None
    assert 'lidercfeny' in wrangler.score_resident_wrangler_target_package_importable_names
    assert wrangler.wrangled_studio_package_importable_names == []
    assert 'lidercfeny' in wrangler.wrangled_score_package_importable_names
