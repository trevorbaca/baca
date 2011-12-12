import baca


def test_MenuSection_indent_level_01():

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section'
    section.extend(['apple', 'banana', 'cherry'])

    assert section.indent_level == 1
