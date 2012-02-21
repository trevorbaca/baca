import baca


def test_MaterialPackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_wrangler
    assert not wrangler.session.is_in_score
    
    assert wrangler.breadcrumb == 'materials'

    assert 'baca.materials' in wrangler.asset_container_importable_names
    assert 'aracilik.mus.materials' in wrangler.asset_container_importable_names

    assert wrangler.current_asset_container_importable_name == 'baca.materials'

    assert wrangler.score_external_asset_container_importable_name == 'baca.materials'
    assert wrangler.score_external_asset_container_initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/__init__.py'
    assert wrangler.score_external_asset_container_path_name == \
        '/Users/trevorbaca/Documents/other/baca/materials'

    assert 'red notes' in wrangler.score_external_wrangled_asset_human_readable_names
    assert 'baca.materials.red_notes' in wrangler.score_external_wrangled_asset_importable_names
    assert '/Users/trevorbaca/Documents/other/baca/materials/red_notes' in \
        wrangler.score_external_wrangled_asset_path_names
    assert 'red_notes' in wrangler.score_external_wrangled_asset_short_names

    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.materials'

    assert wrangler.temporary_asset_importable_name == 'baca.materials.__temporary_package'
    assert wrangler.temporary_asset_path_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/__temporary_package'
    assert wrangler.temporary_asset_short_name == '__temporary_package'
    

def test_MaterialPackageWrangler_read_only_attributes_02():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_wrangler
    wrangler.session.current_score_package_short_name = 'aracilik'
    assert wrangler.session.is_in_score
    
    assert 'aracilik.mus.materials' in wrangler.asset_container_importable_names
    assert wrangler.current_asset_container_importable_name == 'aracilik.mus.materials'
    assert wrangler.temporary_asset_importable_name == 'aracilik.mus.materials.__temporary_package'
    assert wrangler.temporary_asset_path_name == \
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials/__temporary_package'
