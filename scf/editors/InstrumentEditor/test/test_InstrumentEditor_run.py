from abjad import *
import baca


def test_InstrumentEditor_run_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 q')
    assert studio.ts == (10, (1, 5, 7))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 b q')
    assert studio.ts == (12, (1, 5, 7), (6, 10))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 studio q')
    assert studio.ts == (12, (0, 10), (1, 5, 7))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 foo q')
    assert studio.ts == (12, (1, 5, 7), (8, 10))
