import baca


def test_InstrumentationSpecifierEditor_01():
    '''Main menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '9\nperf\nq'
    studio_interface.manage()

    assert studio_interface.session.transcript[-2] == [
      'Sekka (2007) - performers',
      '',
      '     1: flutist (flute)',
      '',
      '     add: add performer',
      '     del: delete performer',
      '     mv: move performer',
      '']


def test_InstrumentationSpecifierEditor_02():
    '''Main menu to performer menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '9\nperf\n1\nq'
    studio_interface.manage()

    assert studio_interface.session.transcript[-2] == [
      'Sekka (2007) - performers - flutist',
      '',
      '     1: flute',
      '',
      '     add: add instrument',
      '     del: delete instrument',
      '     ren: rename performer',
      '     un: unname performer',
      '']


def test_InstrumentationSpecifierEditor_03():
    '''Main menu to performer menu to instrument menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '9\nperf\n1\n1\nq'
    studio_interface.manage()

    assert studio_interface.session.transcript[-2] == [
      'Sekka (2007) - performers - flutist - flute',
      '',
      "     in: instrument name ('flute')",
      "     inm: instrument name markup (Markup('Flute'))",
      "     sin: short instrument name ('fl.')",
      "     sinm: short instrument name markup (Markup('Fl.'))",
      '']
