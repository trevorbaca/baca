import baca


def test_Menu_menu_entry_keys_01():

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section()
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    section_2 = menu.make_new_section()
    section_2.menu_entry_tokens.append(('add', 'add something'))
    section_2.menu_entry_tokens.append(('del', 'delete something'))
    section_2.menu_entry_tokens.append(('mod', 'modify something'))
    assert menu.menu_entry_keys[-6:] == section_1.menu_entry_keys + section_2.menu_entry_keys
