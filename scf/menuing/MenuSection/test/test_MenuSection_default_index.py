import baca
import py


def test_MenuSection_default_index_01():

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section'
    section.extend(['apple', 'banana', 'cherry'])

    assert section.default_index is None
    assert py.test.raises(ValueError, 'section.default_index = -1')
    assert py.test.raises(ValueError, 'section.default_index = 99')
    
    section.default_index = 2
    assert section.default_index == 2
