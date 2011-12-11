from abjad import *
import baca


def test_PerformerEditor_run_01():
    '''Quit, back, studio and junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 q')
    assert studio.ts == (8, (1, 5))
    
    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 b q')
    assert studio.ts == (10, (1, 5), (4, 8))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 studio q')
    assert studio.ts == (10, (0, 8), (1, 5))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 foo q')
    assert studio.ts == (10, (1, 5), (6, 8))
