import baca


def test_MenuSection_menu_entry_return_values_01():
    '''Menu entry return values equal menu entry tokens when menu entry tokens are strings.
    Always true, including for all four combinations of the two settings tested here.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section.use_menu_entry_key_as_menu_entry_return_value = True
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section.use_menu_entry_key_as_menu_entry_return_value = True
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section.use_menu_entry_key_as_menu_entry_return_value = False
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section.use_menu_entry_key_as_menu_entry_return_value = False
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens


def test_MenuSection_menu_entry_return_values_02():
    '''Menu entry return values vary when menu entry tokens are tuples.
    You can explicitly demand a return value equal either to the menu entry key or body.
    Note that section numbering plays no role in this.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    section.use_menu_entry_key_as_menu_entry_return_value = True
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add', 'del', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    section.use_menu_entry_key_as_menu_entry_return_value = True
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add', 'del', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section(is_numbered=True)
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    section.use_menu_entry_key_as_menu_entry_return_value = False
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))
    section.use_menu_entry_key_as_menu_entry_return_value = False
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies
