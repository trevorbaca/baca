import baca


def test_MaterialPackageMakerWrangler_01():
    '''Attributes.
    '''

    material_proxy_wrangler = baca.scf.wranglers.MaterialPackageMakerWrangler()

    assert material_proxy_wrangler.class_name == 'MaterialPackageMakerWrangler'
    assert material_proxy_wrangler.toplevel_global_package_importable_name == 'baca.scf.makers'
    assert material_proxy_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/wranglers/MaterialPackageMakerWrangler/MaterialPackageMakerWrangler.py'
    assert material_proxy_wrangler.spaced_class_name == 'material package maker wrangler'
