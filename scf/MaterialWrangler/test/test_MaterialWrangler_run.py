import baca


def test_MaterialWrangler_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.ts == (4,)

    studio.run(user_input='m b q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='m studio q')
    assert studio.ts == (6, (0, 4))

    # TODO: make this work by causing score backtracking to be ignored
    #studio.run(user_input='m score q')
    #assert studio.ts == (6, (2, 4))

    studio.run(user_input='m asdf q')
    assert studio.ts == (6, (2, 4))


def test_MaterialWrangler_run_02():
    '''Breadcrumbs work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.transcript[-2][0] == 'Studio - materials'
