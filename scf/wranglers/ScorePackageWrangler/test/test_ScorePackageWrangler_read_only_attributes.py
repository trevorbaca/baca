import baca


def test_ScorePackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler

    assert wrangler.current_containing_directory_name == wrangler.scores_directory_name
    assert wrangler.has_toplevel_packages
    assert wrangler.has_wrangled_packages
    assert 'Lidércfény (2008)' in wrangler.score_titles_with_years_to_display 
    assert wrangler.temporary_package_directory_name.endswith('__temporary_package')
    assert wrangler.toplevel_wrangler_target_package_importable_name is None
    assert 'lidercfeny' in wrangler.wrangler_target_package_importable_names
    assert wrangler.wrangled_score_package_importable_name_prefix is None
    assert 'lidercfeny' in wrangler.score_resident_wrangler_target_package_importable_names
    assert wrangler.wrangled_studio_package_importable_names == []
    assert 'lidercfeny' in wrangler.wrangled_score_package_importable_names
