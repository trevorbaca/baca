import baca


def test_InstrumentationEditor_run_01():
    '''Quit works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '9 perf q'
    studio.run()

    assert studio.session.transcript[-2] == [
      'Sekka (2007) - performers & instrumentation',
      '',
      '     1: flutist (flute)',
      '',
      '     add: add performer',
      '     del: delete performer',
      '']


def test_InstrumentationEditor_run_02():
    '''Back works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf b q'
    studio.run()
    transcript = studio.session.transcript

    assert len(transcript) == 8
    assert transcript[2] == transcript[6]


def test_InstrumentationEditor_run_03():
    '''Studio works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf studio q'
    studio.run()
    transcript = studio.session.transcript

    assert len(transcript) == 8
    assert transcript[0] == transcript[6]


def test_InstrumentationEditor_run_04():
    '''Junk works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf foo q'
    studio.run()
    transcript = studio.session.transcript

    assert len(transcript) == 8
    assert transcript[-2] == transcript[-4]


