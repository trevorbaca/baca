import baca


def test_ScorePackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler

    assert wrangler.current_wrangler_target_directory_name == wrangler.scores_directory_name
    assert 'Lidércfény (2008)' in wrangler.score_titles_with_years_to_display 
    assert wrangler.temporary_package_directory_name.endswith('__temporary_package')
    assert wrangler.score_external_wrangler_target_package_importable_name is None
    assert 'lidercfeny' in wrangler.wrangler_target_package_importable_names
    assert wrangler.score_internal_wrangler_target_package_importable_name_suffix is None
    assert 'lidercfeny' in \
        wrangler.list_score_internal_wrangler_target_package_importable_names()
    assert wrangler.score_externalwrangled_package_importable_names == []
    assert 'lidercfeny' in wrangler.list_score_internal_wrangled_package_importable_names()
