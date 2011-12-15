import baca


def test_PerformerEditor_base_states_01():
    '''Start-up, name, set name to none.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar ren None q')
    transcript = editor.transcript
    entry_index = -1

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['Performer',
     '',
     '     Instruments',
     '',
     '     add instruments',
     '     name performer',
     '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['SCF> name', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['Performer name> foo', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['Foo',
     '',
     '     Instruments',
     '',
     '     add instruments',
     '     rename performer',
     '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['SCF> ren', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['New performer name> bar', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['Bar',
     '',
     '     Instruments',
     '',
     '     add instruments',
     '     rename performer',
     '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['SCF> ren', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['New performer name> None', '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['Performer',
     '',
     '     Instruments',
     '',
     '     add instruments',
     '     name performer',
     '']

    entry_index = entry_index + 1
    transcript[entry_index] == \
    ['SCF> q', '']
