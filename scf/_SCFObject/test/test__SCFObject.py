import baca


def test__SCFObject_01():

    scf = baca.scf._SCFObject._SCFObject()
    assert scf.class_name == '_SCFObject'
    assert scf.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/_SCFObject/_SCFObject.py'
