import baca


def test_ScorePackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler

    assert wrangler.breadcrumb == 'scores'

    assert wrangler.current_wrangler_target_directory_name == wrangler.scores_directory_name
    assert wrangler.current_wrangler_target_package_importable_name is None

    assert wrangler.score_external_wrangled_package_importable_names == []
    assert wrangler.score_external_wrangler_target_package_importable_name is None

    assert wrangler.score_internal_wrangler_target_package_importable_name_suffix is None

    assert wrangler.temporary_package_importable_name == '__temporary_package'

    assert 'lidercfeny' in wrangler.wrangler_target_package_importable_names

    assert 'Lidércfény (2008)' in wrangler.visible_score_titles_with_years 
