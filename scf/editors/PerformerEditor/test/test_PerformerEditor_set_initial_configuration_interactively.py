import baca


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add 1 q')
    assert len(studio.transcript) == 10

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add 1 b q')
    transcript = studio.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-6]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add 1 studio q')
    transcript = studio.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-12]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add 1 foo q')
    transcript = studio.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-4]
