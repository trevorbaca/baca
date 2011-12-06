import baca


def test_InstrumentationEditor_screen_shots_01():
    '''Naked startup.
    '''
    
    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='q')
    assert editor.session.transcript == \
    [['Performers & instrumentation',
      '',
      '     add: add performer',
      ''],
     ['SCF> q', '']]
