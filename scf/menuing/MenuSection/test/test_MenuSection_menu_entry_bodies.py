import baca


def test_MenuSection_menu_entry_bodies_01():
    '''Menu entry bodies equal menu entry tokens when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])

    assert not section.is_numbered
    assert section.menu_entry_bodies == ['apple', 'banana', 'cherry']
    assert section.menu_entry_bodies == section.menu_entry_tokens

    section.is_numbered = True
    assert section.is_numbered
    assert section.menu_entry_bodies == ['apple', 'banana', 'cherry']
    assert section.menu_entry_bodies == section.menu_entry_tokens


def test_MenuSection_menu_entry_bodies_02():
    '''Menu entry bodies equal index 1 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section title'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    
    assert not section.is_numbered
    assert section.menu_entry_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_bodies == [x[1] for x in section.menu_entry_tokens]

    section.is_numbered = True
    assert section.is_numbered
    assert section.menu_entry_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_bodies == [x[1] for x in section.menu_entry_tokens]
