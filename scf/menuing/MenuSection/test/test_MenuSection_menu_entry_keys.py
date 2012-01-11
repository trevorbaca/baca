import baca


def test_MenuSection_menu_entry_keys_01():
    '''Menu entry keys equal none when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.is_numbered
    assert section.menu_entry_keys == [None, None, None]

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.section_title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert section.is_numbered
    assert section.menu_entry_keys == [None, None, None]


def test_MenuSection_menu_entry_keys_02():
    '''Menu entry keys equal index 0 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section title'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    assert not section.is_numbered
    assert section.menu_entry_keys == ['add', 'del', 'mod']
    assert section.menu_entry_keys == [x[0] for x in section.tokens]

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.section_title = 'section title'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    assert section.is_numbered
    assert section.menu_entry_keys == ['add', 'del', 'mod']
    assert section.menu_entry_keys == [x[0] for x in section.tokens]
