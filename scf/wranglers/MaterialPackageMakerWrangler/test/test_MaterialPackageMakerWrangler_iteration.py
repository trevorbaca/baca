import baca

studio = baca.scf.studio.Studio()
wrangler = studio.material_package_maker_wrangler


def test_MaterialPackageMakerWrangler_iteration_01():

    assert wrangler.list_score_internal_wrangled_asset_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_02():

    assert wrangler.list_score_internal_asset_container_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_03():

    assert 'PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_visible_asset_short_names()


def test_MaterialPackageMakerWrangler_iteration_04():

    assert 'baca.scf.makers.PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_wrangled_asset_importable_names()
    

def test_MaterialPackageMakerWrangler_iteration_05():

    assert ('PitchRangeInventoryMaterialPackageMaker', 
        'pitch range inventory material package maker') in wrangler.list_wrangled_asset_menuing_pairs()


def test_MaterialPackageMakerWrangler_iteration_06():

    assert 'PitchRangeInventoryMaterialPackageMaker' in wrangler.list_wrangled_package_short_names()

    
def test_MaterialPackageMakerWrangler_iteration_07():

    assert 'PitchRangeInventoryMaterialPackageMaker' in wrangler.list_wrangled_asset_human_readable_names()
