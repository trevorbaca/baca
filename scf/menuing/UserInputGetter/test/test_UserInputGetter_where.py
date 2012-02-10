import baca


def test_UserInputGetter_where_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup performers move where q') 
    assert studio.ts == (11,)
