import scf


def test_SCFObject_public_methods_01():

    scf_object = scf.core.SCFObject()

    assert scf_object.module_importable_name_to_path_name('scf.studio.Studio.Studio') == \
        '/Users/trevorbaca/Documents/other/baca/scf/studio/Studio/Studio.py'
    assert scf_object.package_exists('scf')    
    assert scf_object.package_importable_name_to_path_name('scf') == \
        '/Users/trevorbaca/Documents/other/baca/scf'
