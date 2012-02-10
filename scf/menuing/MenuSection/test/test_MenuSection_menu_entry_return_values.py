import baca


def test_MenuSection_menu_entry_return_values_01():
    '''Menu entry return values equal menu entry tokens when menu entry tokens are strings.
    Always true, including for all four combinations of the two settings tested here.
    '''

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    section.return_value_attribute = 'body'
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    section.return_value_attribute = 'body'
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens


def test_MenuSection_menu_entry_return_values_02():
    '''Menu entry return values vary when menu entry tokens are tuples.
    You can explicitly demand a return value equal either to the menu entry key or body.
    Note that section numbering plays no role in this.
    '''

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add', 'del', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add', 'del', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    section.return_value_attribute = 'body'
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies

    menu = baca.scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('del', 'delete something'))
    section.append(('mod', 'modify something'))
    section.return_value_attribute = 'body'
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies
