import baca


def test_UserInputGetter_score_01():

    studio = baca.scf.studiopackage.Studio()
    studio.run(user_input='1 setup performers move sco q')
    assert studio.ts == (11, (2, 9))
