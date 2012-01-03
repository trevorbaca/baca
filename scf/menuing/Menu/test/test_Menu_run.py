import baca


def test_Menu_run_01():
    '''String tokens with default settings.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']


def test_Menu_run_02():
    '''Turning off keys does nothing to string tokens.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']


def test_Menu_run_03():
    '''Hidding suppresses output.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location', '']


def test_Menu_run_04():
    '''String tokens with numbering turned on.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: apple',
      '     2: banana',
      '     3: cherry',
      '']


def test_Menu_run_05():
    '''Turning ranges on without numbering does nothing.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.extend(['apple', 'banana', 'cherry'])
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']


def test_Menu_run_06():
    '''Tuple tokens with default settings.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1 = menu.make_new_section()
    section_1.menu_entry_tokens.append(('add', 'add something'))
    section_1.menu_entry_tokens.append(('del', 'delete something'))
    section_1.menu_entry_tokens.append(('mod', 'modify something'))
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     add something (add)',
      '     delete something (del)',
      '     modify something (mod)',
      '']


def test_Menu_run_07():
    '''Tuple tokens with keys turned off.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'add something'))
    section_1.menu_entry_tokens.append(('del', 'delete something'))
    section_1.menu_entry_tokens.append(('mod', 'modify something'))
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     add something',
      '     delete something',
      '     modify something',
      '']


def test_Menu_run_08():
    '''Hidding suppresses output.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'add something'))
    section_1.menu_entry_tokens.append(('del', 'delete something'))
    section_1.menu_entry_tokens.append(('mod', 'modify something'))
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location', '']


def test_Menu_run_09():
    '''Tuple tokens with numbering turned on.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'add something'))
    section_1.menu_entry_tokens.append(('del', 'delete something'))
    section_1.menu_entry_tokens.append(('mod', 'modify something'))
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: add something (add)',
      '     2: delete something (del)',
      '     3: modify something (mod)',
      '']


def test_Menu_run_10():
    '''Turning ranges on without numbering does nothing.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'add something'))
    section_1.menu_entry_tokens.append(('del', 'delete something'))
    section_1.menu_entry_tokens.append(('mod', 'modify something'))
    menu.run(user_input='q')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     add something (add)',
      '     delete something (del)',
      '     modify something (mod)',
      '']
