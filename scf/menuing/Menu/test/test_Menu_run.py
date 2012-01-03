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
    section_1.menu_entry_tokens.append(('add', 'first command'))
    section_1.menu_entry_tokens.append(('del', 'second command'))
    section_1.menu_entry_tokens.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (del)',
      '     third command (mod)',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-del')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_07():
    '''Tuple tokens with keys turned off.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'first command'))
    section_1.menu_entry_tokens.append(('del', 'second command'))
    section_1.menu_entry_tokens.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command',
      '     second command',
      '     third command',
      '']

    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-del')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_08():
    '''Hidding suppresses output.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'first command'))
    section_1.menu_entry_tokens.append(('del', 'second command'))
    section_1.menu_entry_tokens.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location', '']

    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-del')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_09():
    '''Tuple tokens with numbering turned on.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'first command'))
    section_1.menu_entry_tokens.append(('del', 'second command'))
    section_1.menu_entry_tokens.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: first command (add)',
      '     2: second command (del)',
      '     3: third command (mod)',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-del')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_10():
    '''Turning ranges on without numbering does nothing.
    '''

    menu = baca.scf.menuing.Menu()
    menu.append_breadcrumb('location')
    section_1 = menu.make_new_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True)
    section_1.section_title = 'section'
    section_1.menu_entry_tokens.append(('add', 'first command'))
    section_1.menu_entry_tokens.append(('del', 'second command'))
    section_1.menu_entry_tokens.append(('mod', 'third command'))
    result = menu.run(user_input='foo') 

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (del)',
      '     third command (mod)',
      '']
    assert result == []

    # TODO:
    menu.session.reinitialize()
    result = menu.run(user_input='q')
    # current behavior: assert result is None
    # correct behavior: assert result == []

    # TODO:
    menu.session.reinitialize()
    result = menu.run(user_input='1')
    # current behavior: #assert result == ['add']
    # correct behavior: assert result == []

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == ['add']

    # TODO:
    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    # current behavior: assert result == []
    # correct behavior: assert result == ['add']

    # TODO:
    result = menu.run(user_input='1, 3-2')
    # current behavior: assert result == ['add', 'mod', 'del']
    # correct behavior: assert result == []

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-del')
    assert result == ['add', 'mod', 'del']

    # TODO:
    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    # current behavior: assert result == []
    # correct behavior: assert result == ['add', 'mod', 'del']

    # TODO:
    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    # current behavior: assert result == []
    # correct behavior: assert result == ['add', 'mod', 'del']
