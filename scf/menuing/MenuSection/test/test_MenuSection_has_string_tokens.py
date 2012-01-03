import baca


def test_MenuSection_has_string_tokens_01():

    menu = baca.scf.menuing.Menu()
    section = menu.make_new_section()
    assert not section.has_string_tokens

    section  = menu.make_new_section()
    section.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    assert section.has_string_tokens

    section  = menu.make_new_section()
    section.menu_entry_tokens.append(('add', 'first command'))
    section.menu_entry_tokens.append(('del', 'second command'))
    section.menu_entry_tokens.append(('mod', 'third command'))
    assert not section.has_string_tokens
