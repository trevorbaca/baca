import baca


def test_MaterialPackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.home_package_proxy.material_package_wrangler
    
    assert wrangler.breadcrumb == 'materials'
    assert wrangler.current_containing_package_importable_name == 'baca.materials'


def test_MaterialPackageWrangler_read_only_attributes_02():

    studio = baca.scf.studio.Studio()
    wrangler = studio.home_package_proxy.material_package_wrangler
    
    assert wrangler.breadcrumb == 'materials'
    assert wrangler.current_containing_package_importable_name == 'baca.materials'
