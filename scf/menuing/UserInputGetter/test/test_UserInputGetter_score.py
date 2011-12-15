import baca


def test_UserInputGetter_score_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf move sco q')
    assert studio.ts == (9, (2, 7))
