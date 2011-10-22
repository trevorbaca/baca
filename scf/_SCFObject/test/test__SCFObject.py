import baca


def test__SCFObject_01():

    scf = baca.scf._SCFObject._SCFObject()

    assert scf.baca_directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert scf.baca_materials_directory_name == '/Users/trevorbaca/Documents/other/baca/materials'
    assert scf.baca_materials_package_importable_name == 'baca.materials'
    assert scf.baca_materials_package_short_name == 'materials'
    assert scf.class_name == '_SCFObject'
    assert scf.makers_directory_name == '/Users/trevorbaca/Documents/other/baca/makers'
    assert scf.scores_directory_name == '/Users/trevorbaca/Documents/scores'
    assert scf.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/_SCFObject/_SCFObject.py'
