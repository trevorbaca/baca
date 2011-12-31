import baca


def test_MenuSection_menu_entry_keys_01():
    '''Menu entry keys equal none when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])

    assert not section.number_menu_entries
    assert section.menu_entry_keys == [None, None, None]

    section.number_menu_entries = True
    assert section.number_menu_entries
    assert section.menu_entry_keys == [None, None, None]


def test_MenuSection_menu_entry_keys_02():
    '''Menu entry keys equal index 0 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.section_title = 'section title'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))

    assert not section.number_menu_entries
    assert section.menu_entry_keys == ['add', 'del', 'mod']
    assert section.menu_entry_keys == [x[0] for x in section.menu_entry_tokens]

    section.number_menu_entries = True
    assert section.number_menu_entries
    assert section.menu_entry_keys == ['add', 'del', 'mod']
    assert section.menu_entry_keys == [x[0] for x in section.menu_entry_tokens]
