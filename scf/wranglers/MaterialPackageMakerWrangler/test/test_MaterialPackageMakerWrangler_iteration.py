import baca

studio = baca.scf.studio.Studio()
wrangler = studio.material_package_maker_wrangler


def test_MaterialPackageMakerWrangler_iteration_01():

    assert wrangler.list_score_internal_asset_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_02():

    assert wrangler.list_score_internal_asset_container_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_04():

    assert 'baca.scf.makers.PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_asset_importable_names()
    

def test_MaterialPackageMakerWrangler_iteration_05():

    assert ('baca.scf.makers.PitchRangeInventoryMaterialPackageMaker', 
        'pitch range inventory material package maker') in wrangler.list_visible_asset_menuing_pairs()


def test_MaterialPackageMakerWrangler_iteration_06():

    assert 'pitch range inventory material package maker' in wrangler.list_asset_human_readable_names()
