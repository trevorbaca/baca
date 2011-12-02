from abjad import *
import baca


def test_PerformerEditor_01():
    '''Main menu.
    '''


    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'q'
    performer_editor.edit_interactively()

    assert len(performer_editor.session.transcript) == 2
    assert performer_editor.session.transcript[0] == [
    'Performer',
      '',
      '     add: add instrument',
      '     del: delete instrument',
      '     name: name performer',
      '']


def test_PerformerEditor_02():
    '''Target creation.
    '''


    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'q'
    performer_editor.edit_interactively()
    assert isinstance(performer_editor.target, type(scoretools.Performer()))


def test_PerformerEditor_03():
    '''Quit while adding instrument.
    '''

    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'add\nq'
    performer_editor.edit_interactively()
    transcript = performer_editor.session.transcript
    
    assert len(transcript) == 4 
    assert transcript[2][:4] == [
      'Performer - select instrument',
      '',
      '     1: accordion',
      '     2: alto flute']


def test_PerformerEditor_04():
    '''Back while adding instrument.
    '''

    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'add\nb\nq'
    performer_editor.edit_interactively()
    transcript = performer_editor.session.transcript

    assert len(transcript) == 6 
    assert transcript[0] == transcript[4]
