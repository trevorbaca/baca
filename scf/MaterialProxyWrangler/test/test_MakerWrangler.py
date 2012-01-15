import baca


def test_MaterialProxyWrangler_01():
    '''Attributes.
    '''

    maker_wrangler = baca.scf.MaterialProxyWrangler()

    assert maker_wrangler.class_name == 'MaterialProxyWrangler'
    assert maker_wrangler.directory_name == '/Users/trevorbaca/Documents/other/baca/scf/materialproxies'
    assert maker_wrangler.has_directory
    assert maker_wrangler.has_initializer
    assert maker_wrangler.initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/materialproxies/__init__.py'
    assert maker_wrangler.package_importable_name == 'baca.scf.materialproxies'
    assert maker_wrangler.package_short_name == 'materialproxies'
    assert maker_wrangler.package_spaced_name == 'materialproxies'
    assert maker_wrangler.score is None
    assert maker_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/MaterialProxyWrangler/MaterialProxyWrangler.py'
    assert maker_wrangler.spaced_class_name == 'material proxy wrangler'


def test_MaterialProxyWrangler_02():
    '''Iteration.
    '''

    maker_wrangler = baca.scf.MaterialProxyWrangler()
