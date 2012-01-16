import baca


def test_PackageWrangler_01():
    '''Attributes.
    '''

    package_wrangler = baca.scf.PackageWrangler('/Users/trevorbaca/Documents/other/baca')
   
    assert package_wrangler.class_name == 'PackageWrangler'
    assert package_wrangler.directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert package_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/PackageWrangler/PackageWrangler.py'
    assert package_wrangler.spaced_class_name == 'package wrangler'
