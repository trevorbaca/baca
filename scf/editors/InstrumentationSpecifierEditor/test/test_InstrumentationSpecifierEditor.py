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


