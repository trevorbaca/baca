import baca


def test_InstrumentationEditor_traversal_01():
    '''Instrumentation editor to performer editor.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '9 perf 1 q'
    studio.run()

    assert studio.session.transcript[-2] == [
      'Sekka (2007) - performers & instrumentation - flutist',
      '',
      '     1: flute',
      '',
      '     add: add instrument',
      '     del: delete instrument',
      '     ren: rename performer',
      '     un: unname performer',
      '']


def test_InstrumentationEditor_traversal_02():
    '''Instrumentation editor to performer editor to instrument editor.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '9 perf 1 1 q'
    studio.run()

    assert studio.session.transcript[-2] == [
      'Sekka (2007) - performers & instrumentation - flutist - flute',
      '',
      "     in: instrument name ('flute')",
      "     inm: instrument name markup (Markup('Flute'))",
      "     sin: short instrument name ('fl.')",
      "     sinm: short instrument name markup (Markup('Fl.'))",
      '']
