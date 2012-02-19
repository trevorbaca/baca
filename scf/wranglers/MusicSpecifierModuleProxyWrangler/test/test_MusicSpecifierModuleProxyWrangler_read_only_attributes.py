import baca


def test_MusicSpecifierModuleProxyWrangler_read_only_attributes_01():

    wrangler = baca.scf.wranglers.MusicSpecifierModuleProxyWrangler()
    assert wrangler.breadcrumb == 'music specifiers'
    assert wrangler.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/specifiers/__init__.py'
    assert wrangler.toplevel_studio_package_importable_name == 'baca.specifiers'
    assert wrangler.wrangled_score_package_importable_name_prefix == 'mus.specifiers'
    
