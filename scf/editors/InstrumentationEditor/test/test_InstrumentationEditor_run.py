import baca


def test_InstrumentationEditor_run_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf q'
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 6

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf b q'
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 8
    assert transcript[2] == transcript[6]

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf studio q'
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 8
    assert transcript[0] == transcript[6]

    studio = baca.scf.Studio()
    studio.session.user_input = '1 perf foo q'
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 8
    assert transcript[-2] == transcript[-4]
