import baca


def test_UserInputGetter_studio_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf move stu q')
    assert studio.ts == (9, (0, 7))
