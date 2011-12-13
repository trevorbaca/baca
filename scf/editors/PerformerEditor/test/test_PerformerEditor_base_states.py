import baca


def test_PerformerEditor_base_states_01():
    '''Start-up, name, set name to none.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar ren None q')
    assert editor.transcript == \
    [['Performer',
      '',
      '     Instruments',
      '',
      '     add instruments',
      '     name performer',
      ''],
     ['SCF> name', ''],
     ['Performer name> foo', ''],
     ['Foo',
      '',
      '     Instruments',
      '',
      '     add instruments',
      '     rename performer',
      ''],
     ['SCF> ren', ''],
     ['New performer name> bar', ''],
     ['Bar',
      '',
      '     Instruments',
      '',
      '     add instruments',
      '     rename performer',
      ''],
     ['SCF> ren', ''],
     ['New performer name> None', ''],
     ['Performer',
      '',
      '     Instruments',
      '',
      '     add instruments',
      '     name performer',
      ''],
     ['SCF> q', '']]
