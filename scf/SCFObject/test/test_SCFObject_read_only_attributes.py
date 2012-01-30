import baca
import types


def test_SCFObject_read_only_attributes_01():
    '''SCF object attributes.
    '''

    scf = baca.scf.SCFObject.SCFObject()

    assert scf.class_name == 'SCFObject'
    assert scf.help_item_width == 5
    assert isinstance(scf.helpers, types.ModuleType)
    assert scf.spaced_class_name == 's c f object'
    assert scf.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/SCFObject/SCFObject.py'
