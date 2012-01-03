import baca


def test_MaterialProxy_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m sargasso q')
    assert studio.ts == (6,)

    studio.run(user_input='m sargasso b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='m sargasso studio q')
    assert studio.ts == (8, (0, 6))

    # TODO: make this work by causing score backtracking to be ignored
    #studio.run(user_input='m sargasso score q')
    #assert studio.ts == (8, (4, 6))

    studio.run(user_input='m sargasso foo q')
    assert studio.ts == (8, (4, 6))


def test_MaterialProxy_run_02():
    '''Breadcrumbs work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m sargasso q')
    assert studio.transcript[-2][0] == 'Studio - materials - sargasso multipliers'
