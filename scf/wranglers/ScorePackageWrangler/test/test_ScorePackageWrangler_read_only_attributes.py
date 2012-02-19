import baca


def test_ScorePackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler

    assert wrangler.has_toplevel_packages
    assert wrangler.has_wrangled_packages
    assert 'lidercfeny' in wrangler.score_package_short_names
    assert 'lidercfeny' in wrangler.score_package_short_names_to_display
    assert baca.scf.proxies.ScorePackageProxy('lidercfeny') in wrangler.score_package_proxies_to_display
    assert 'Lidércfény (2008)' in wrangler.score_titles_with_years 
    assert wrangler.temporary_score_package_directory_name.endswith('__temporary_score_package')
    assert wrangler.toplevel_global_package_importable_name is None
    assert 'lidercfeny' in wrangler.toplevel_package_importable_names
    assert wrangler.toplevel_score_package_importable_name_body == ''
    assert 'lidercfeny' in wrangler.toplevel_score_package_importable_names
    assert wrangler.wrangled_global_package_importable_names == []
    assert 'lidercfeny' in wrangler.wrangled_score_package_importable_names
