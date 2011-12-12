import baca


def test_MenuSection_has_tuple_tokens_01():

    menu = baca.scf.menuing.Menu()
    section = menu.make_new_section()
    assert not section.has_tuple_tokens

    section  = menu.make_new_section()
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.has_tuple_tokens

    section  = menu.make_new_section()
    section.append(('add', 'first command'))
    section.append(('del', 'second command'))
    section.append(('mod', 'third command'))
    assert section.has_tuple_tokens
