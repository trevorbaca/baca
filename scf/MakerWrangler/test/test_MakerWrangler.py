import baca


def test_MakerWrangler_01():
    '''Attributes.
    '''

    maker_wrangler = baca.scf.MakerWrangler()

    assert maker_wrangler.class_name == 'MakerWrangler'
    assert maker_wrangler.directory_name == '/Users/trevorbaca/Documents/other/baca/makers'
    assert maker_wrangler.has_directory
    assert maker_wrangler.has_initializer
    assert maker_wrangler.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/makers/__init__.py'
    assert maker_wrangler.package_importable_name == 'baca.makers'
    assert maker_wrangler.package_short_name == 'makers'
    assert maker_wrangler.package_spaced_name == 'makers'
    assert maker_wrangler.score is None
    assert maker_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/MakerWrangler/MakerWrangler.py'
    assert maker_wrangler.spaced_class_name == 'maker wrangler'


def test_MakerWrangler_02():
    '''Iteration.
    '''

    maker_wrangler = baca.scf.MakerWrangler()
