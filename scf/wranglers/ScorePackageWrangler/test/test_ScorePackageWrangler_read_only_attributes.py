import scf

studio = scf.studio.Studio()
wrangler = studio.score_package_wrangler


def test_ScorePackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler.breadcrumb == 'scores'


def test_ScorePackageWrangler_read_only_attributes_02():
    '''Asset containers (all).
    '''

    assert 'lidercfeny' in wrangler.list_asset_container_importable_names()
    assert '/Users/trevorbaca/Documents/scores/lidercfeny' in wrangler.list_asset_container_path_names()


def test_ScorePackageWrangler_read_only_attributes_03():
    '''Current asset container.
    '''

    assert wrangler.current_asset_container_importable_name is None
    assert wrangler.current_asset_container_path_name == wrangler.scores_directory_name


def test_ScorePackageWrangler_read_only_attributes_04():
    '''Score-external asset container.
    '''

    assert wrangler.list_score_external_asset_container_importable_names() == []


def test_ScorePackageWrangler_read_only_attributes_05():
    '''Score-external assets.
    '''

    assert wrangler.list_score_external_asset_importable_names() == []


def test_ScorePackageWrangler_read_only_attributes_06():
    '''Infix.
    '''

    assert wrangler.score_internal_asset_container_importable_name_infix is None


def test_ScorePackageWrangler_read_only_attributes_07():
    '''Temporary asset.
    '''

    assert wrangler.temporary_asset_importable_name == '__temporary_package'


def test_ScorePackageWrangler_read_only_attributes_08():
    '''Other read-only attributes.
    '''

    assert 'Lidércfény (2008)' in wrangler.visible_score_titles_with_years
