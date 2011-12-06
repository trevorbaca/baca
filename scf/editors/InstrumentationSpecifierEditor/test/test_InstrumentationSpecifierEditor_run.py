import baca


def test_InstrumentationSpecifierEditor_run_01():
    '''Quit works.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '9 perf q'
    studio_interface.run()

    assert studio_interface.session.transcript[-2] == [
      'Sekka (2007) - performers & instrumentation',
      '',
      '     1: flutist (flute)',
      '',
      '     add: add performer',
      '     del: delete performer',
      '']


def test_InstrumentationSpecifierEditor_run_02():
    '''Back works.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '1 perf b q'
    studio_interface.run()
    transcript = studio_interface.session.transcript

    assert len(transcript) == 8
    assert transcript[2] == transcript[6]


def test_InstrumentationSpecifierEditor_run_03():
    '''Studio works.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '1 perf studio q'
    studio_interface.run()
    transcript = studio_interface.session.transcript

    assert len(transcript) == 8
    assert transcript[0] == transcript[6]


def test_InstrumentationSpecifierEditor_run_04():
    '''Junk works.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.user_input = '1 perf foo q'
    studio_interface.run()
    transcript = studio_interface.session.transcript

    assert len(transcript) == 8
    assert transcript[-2] == transcript[-4]


