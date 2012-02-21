import baca


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_maker_wrangler

    assert wrangler.breadcrumb == 'material package makers'
    assert wrangler.current_asset_container_package_importable_name == 'baca.scf.makers'
    assert all([
        x.startswith('baca.scf.makers.') for x in wrangler.score_external_wrangled_asset_importable_names])

    assert wrangler.score_external_asset_container_importable_name == 'baca.scf.makers'
    assert wrangler.score_internal_asset_container_importable_name_suffix is None

    assert wrangler.temporary_package_importable_name == 'baca.scf.makers.__temporary_package'

    assert wrangler.asset_container_package_importable_names == ['baca.scf.makers']
