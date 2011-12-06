from abjad import *
import baca


def test_PerformerEditor_run_01():
    '''Quit, back, studio and junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 q')
    assert len(studio.transcript) == 8
    
    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 b q')
    transcript = studio.transcript
    assert len(transcript) == 10
    assert transcript[-4] == transcript[-4] 

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 studio q')
    transcript = studio.transcript
    assert len(transcript) == 10
    assert transcript[-2] == transcript[-10] 

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 foo q')
    transcript = studio.transcript
    assert len(transcript) == 10
    assert transcript[-2] == transcript[-4] 


def test_PerformerEditor_run_02():
    '''Target creation.
    '''

    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'q'
    performer_editor.run()
    assert isinstance(performer_editor.target, type(scoretools.Performer()))
