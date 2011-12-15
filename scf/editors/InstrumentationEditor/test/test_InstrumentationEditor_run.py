import baca


def test_InstrumentationEditor_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf q')
    assert studio.ts == (6,)

    studio.run(user_input='1 perf b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='1 perf studio q')
    assert studio.ts == (8, (0, 6))

    studio.run(user_input='1 perf score q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='1 perf foo q')
    assert studio.ts == (8, (4, 6))
