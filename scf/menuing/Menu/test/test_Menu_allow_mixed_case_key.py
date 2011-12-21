import baca


def test_Menu_allow_mixed_case_key_01():
    '''Allow mixed case 'stu' key.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='arch stu q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='arch STU q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='arch sTu q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='arch sTU q')
    assert studio.ts == (6, (0, 4))
