import baca


def test_UserInputGetter_exec_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup performers move exec 2**30 q')
    assert studio.ts == (12,)
