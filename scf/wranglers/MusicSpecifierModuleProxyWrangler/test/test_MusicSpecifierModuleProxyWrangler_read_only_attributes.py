import baca


def test_MusicSpecifierModuleProxyWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.MusicSpecifierModuleProxyWrangler()
    assert wrangler.breadcrumb == 'music specifiers'
    assert wrangler.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/specifiers/__init__.py'
    assert wrangler.score_external_wrangler_target_package_importable_name == 'baca.specifiers'
    assert wrangler.score_internal_wrangled_package_importable_name_infix == 'mus.specifiers'
    
