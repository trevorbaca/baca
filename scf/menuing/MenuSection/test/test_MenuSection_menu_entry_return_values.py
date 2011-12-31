import baca


# TODO: extend behavior such that section implements use_menu_entry_key_as_menu_entry_return_values
#       and allows for menu keys to be returned here instead of menu bodies
def test_MenuSection_menu_entry_return_values_01():
    '''Menu entry return values equal menu entry tokens when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])

    assert not section.number_menu_entries
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens

    section.number_menu_entries = True
    assert section.number_menu_entries
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.menu_entry_tokens


def test_MenuSection_menu_entry_return_values_02():
    '''Menu entry return values equal index 1 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section = menu.make_new_section()
    section.title = 'section'
    section.menu_entry_tokens.append(('add', 'add something'))
    section.menu_entry_tokens.append(('del', 'delete something'))
    section.menu_entry_tokens.append(('mod', 'modify something'))

    assert not section.number_menu_entries
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies

    section.number_menu_entries = True
    assert section.number_menu_entries
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies
