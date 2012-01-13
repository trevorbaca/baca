import baca


def test_MaterialProxyWrangler_01():
    '''Attributes.
    '''

    material_proxy_wrangler = baca.scf.MaterialProxyWrangler()

    assert material_proxy_wrangler.class_name == 'MaterialProxyWrangler'
    assert material_proxy_wrangler.toplevel_global_package_importable_name == 'baca.scf.materialproxies'
    assert material_proxy_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/MaterialProxyWrangler/MaterialProxyWrangler.py'
    assert material_proxy_wrangler.spaced_class_name == 'material proxy wrangler'
