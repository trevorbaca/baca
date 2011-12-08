import baca


def test_PerformerEditor_base_states_01():
    '''Start-up, name, remove name.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar rpn q')
    assert editor.transcript == \
    [['Performer',
      '',
      '     add: add instrument',
      '     name: name performer',
      ''],
     ['SCF> name', ''],
     ['Performer name> foo', ''],
     ['Foo',
      '',
      '     add: add instrument',
      '     ren: rename performer',
      '     rpn: remove performer name',
      ''],
     ['SCF> ren', ''],
     ['New performer name> bar', ''],
     ['Bar',
      '',
      '     add: add instrument',
      '     ren: rename performer',
      '     rpn: remove performer name',
      ''],
     ['SCF> rpn', ''],
     ['Performer',
      '',
      '     add: add instrument',
      '     name: name performer',
      ''],
     ['SCF> q', '']]
