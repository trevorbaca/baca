import baca


def test_UserInputGetter_back_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf move b q')
    assert studio.ts == (9, (4, 7))
