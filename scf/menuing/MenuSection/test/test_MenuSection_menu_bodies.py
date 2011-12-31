import baca


def test_MenuSection_menu_bodies_01():
    '''Menu bodies work regardless menu entry token type.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section title'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))

    assert section.menu_bodies == ['add something', 'delete something', 'modify something']
