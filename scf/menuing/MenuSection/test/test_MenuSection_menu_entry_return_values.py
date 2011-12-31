import baca


def test_MenuSection_menu_entry_return_values_01():
    '''When section is not numbered, menu entry return values are none.
    True when section houses string menu entry tokens.
    Also true when section houses tuple menu entry tokens.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    assert section.menu_entry_return_values is None

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    assert section.menu_entry_return_values is None


def test_MenuSection_menu_entry_return_values_02():
    '''When section is numbered and when section houses string menu entry tokens,
    then menu entry return values equal menu entry bodies.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section.number_menu_entries = True
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies


def test_MenuSection_menu_entry_return_values_03():
    '''When section is numbered and when section houses tuple menu entry tokens,
    then menu entry return values equal menu entry bodies.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    section.number_menu_entries = True
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies
