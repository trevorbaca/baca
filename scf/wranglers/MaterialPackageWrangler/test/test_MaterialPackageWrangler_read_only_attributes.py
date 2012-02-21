import baca


def test_MaterialPackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_wrangler
    assert not wrangler.session.is_in_score
    
    assert wrangler.breadcrumb == 'materials'
    assert wrangler.current_asset_container_package_importable_name == 'baca.materials'
    assert all([
        x.startswith('baca.materials.') for x in wrangler.score_external_wrangled_asset_importable_names])

    assert wrangler.score_external_asset_container_importable_name == 'baca.materials'
    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.materials'

    assert wrangler.temporary_package_importable_name == 'baca.materials.__temporary_package'

    assert 'baca.materials' in wrangler.asset_container_package_importable_names
    assert 'aracilik.mus.materials' in wrangler.asset_container_package_importable_names

    
def test_MaterialPackageWrangler_read_only_attributes_02():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_wrangler
    wrangler.session.current_score_package_short_name = 'aracilik'
    assert wrangler.session.is_in_score
    
    assert wrangler.breadcrumb == 'materials'

    assert wrangler.current_asset_container_package_importable_name == 'aracilik.mus.materials'

    assert all([
        x.startswith('baca.materials.') for x in wrangler.score_external_wrangled_asset_importable_names])
    assert wrangler.score_external_asset_container_importable_name == 'baca.materials'

    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.materials'

    assert wrangler.temporary_package_importable_name == 'aracilik.mus.materials.__temporary_package'

    assert 'baca.materials' in wrangler.asset_container_package_importable_names
    assert 'aracilik.mus.materials' in wrangler.asset_container_package_importable_names
