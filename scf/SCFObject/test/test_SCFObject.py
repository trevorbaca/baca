import baca
import types


def test_SCFObject_01():
    '''SCF object attributes.
    '''

    scf = baca.scf.SCFObject.SCFObject()

    assert issubclass(scf.Menu, baca.scf.menuing.Menu)
    assert issubclass(scf.MenuSection, baca.scf.menuing.MenuSection)
    assert issubclass(scf.UserInputGetter, baca.scf.menuing.UserInputGetter)

    assert scf.class_name == 'SCFObject'
    assert scf.help_item_width == 5
    assert isinstance(scf.helpers, types.ModuleType)
    assert scf.spaced_class_name == 's c f object'
    assert scf.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/SCFObject/SCFObject.py'


def test_SCFObject_02():
    '''SCF object methods.
    '''

    scf = baca.scf.SCFObject.SCFObject()

    assert scf.make_menu_title(None, 'bar') == 'Bar\n'
    assert scf.make_menu_title('foo', 'bar') == 'Foo - bar\n'
