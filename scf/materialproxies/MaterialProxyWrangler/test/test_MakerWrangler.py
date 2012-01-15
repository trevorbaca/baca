import baca


def test_MaterialProxyWrangler_01():
    '''Attributes.
    '''

    material_proxy_wrangler = baca.scf.materialproxies.MaterialProxyWrangler()

    assert material_proxy_wrangler.class_name == 'MaterialProxyWrangler'
    assert material_proxy_wrangler.directory_name == '/Users/trevorbaca/Documents/other/baca/scf/materialproxies'
    assert material_proxy_wrangler.has_directory
    assert material_proxy_wrangler.has_initializer
    assert material_proxy_wrangler.initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/materialproxies/__init__.py'
    assert material_proxy_wrangler.package_importable_name == 'baca.scf.materialproxies'
    assert material_proxy_wrangler.package_short_name == 'materialproxies'
    assert material_proxy_wrangler.package_spaced_name == 'materialproxies'
    assert material_proxy_wrangler.score is None
    assert material_proxy_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/materialproxies/MaterialProxyWrangler/MaterialProxyWrangler.py'
    assert material_proxy_wrangler.spaced_class_name == 'material proxy wrangler'


def test_MaterialProxyWrangler_02():
    '''Iteration.
    '''

    material_proxy_wrangler = baca.scf.materialproxies.MaterialProxyWrangler()
