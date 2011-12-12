import baca


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add 1 q')
    assert studio.ts == (10, (1, 7))

    studio.run(user_input='1 perf add 1 b q')
    assert studio.ts == (12, (1, 7), (6, 10))

    studio.run(user_input='1 perf add 1 studio q')
    assert studio.ts == (12, (0, 10), (1, 7))

    studio.run(user_input='1 perf add 1 score q')
    assert studio.ts == (12, (1, 7), (2, 10))

    studio.run(user_input='1 perf add 1 foo q')
    assert studio.ts == (12, (1, 7), (8, 10))
