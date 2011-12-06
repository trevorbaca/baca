import baca


def test_InstrumentationSpecifierEditor_add_performer_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf add q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 8

    studio = baca.scf.Studio(user_input='1 perf add b q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 10
    assert transcript[4] == transcript[8]

    studio = baca.scf.Studio(user_input='1 perf add studio q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 10
    assert transcript[0] == transcript[8]

    studio = baca.scf.Studio(user_input='1 perf add foo q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 10
    assert transcript[6] == transcript[8]
