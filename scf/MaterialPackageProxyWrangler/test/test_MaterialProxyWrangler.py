import baca


def test_MaterialPackageProxyWrangler_01():
    '''Attributes.
    '''

    material_proxy_wrangler = baca.scf.MaterialPackageProxyWrangler()

    assert material_proxy_wrangler.class_name == 'MaterialPackageProxyWrangler'
    assert material_proxy_wrangler.toplevel_global_package_importable_name == 'baca.scf.materialproxies'
    assert material_proxy_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/MaterialPackageProxyWrangler/MaterialPackageProxyWrangler.py'
    assert material_proxy_wrangler.spaced_class_name == 'material package proxy wrangler'
