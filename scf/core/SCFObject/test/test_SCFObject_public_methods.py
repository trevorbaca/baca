import baca


def test_SCFObject_public_methods_01():

    scf = baca.scf.core.SCFObject()

    assert scf.module_importable_name_to_full_file_name('baca.scf.studio.Studio.Studio') == \
        '/Users/trevorbaca/Documents/other/baca/scf/studio/Studio/Studio.py'
    assert scf.package_exists('baca.scf')    
    assert scf.package_importable_name_to_directory_name('baca.scf') == \
        '/Users/trevorbaca/Documents/other/baca/scf'
