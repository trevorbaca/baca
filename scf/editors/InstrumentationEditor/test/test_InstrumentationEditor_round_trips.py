import baca


def test_InstrumentationEditor_round_trips_01():
    '''Round trip.
    '''
    
    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 mv 1 2 del 2 q')
    transcript = editor.transcript
    entry_index = -1

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers', '', '     add performers', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> add', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers - add performers',
     '',
     '     1: accordionist',
     '     2: bassist',
     '     3: bassoonist',
     '     4: cellist',
     '     5: clarinetist',
     '     6: flutist',
     '     7: guitarist',
     '     8: harpist',
     '     9: harpsichordist',
     '     10: hornist',
     '     11: oboist',
     '     12: percussionist',
     '     13: pianist',
     '     14: trombonist',
     '     15: trumpeter',
     '     16: tubist',
     '     17: violinist',
     '     18: violist',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> 1', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers - add performers - accordionist',
     '',
     '     Select instruments',
     '',
     '     1: accordion (default)',
     '',
     '     other instruments',
     '     no instruments',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> 1', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     1: accordionist (accordion)',
     '',
     '     add performers',
     '     delete performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> add', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers - add performers',
     '',
     '     1: accordionist',
     '     2: bassist',
     '     3: bassoonist',
     '     4: cellist',
     '     5: clarinetist',
     '     6: flutist',
     '     7: guitarist',
     '     8: harpist',
     '     9: harpsichordist',
     '     10: hornist',
     '     11: oboist',
     '     12: percussionist',
     '     13: pianist',
     '     14: trombonist',
     '     15: trumpeter',
     '     16: tubist',
     '     17: violinist',
     '     18: violist',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> 2', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers - add performers - bassist',
     '',
     '     Select instruments',
     '',
     '     1: contrabass (default)',
     '',
     '     other instruments',
     '     no instruments',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> 1', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     1: accordionist (accordion)',
     '     2: bassist (contrabass)',
     '',
     '     add performers',
     '     delete performers',
     '     move performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> mv', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Old number> 1', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['New number> 2', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     1: bassist (contrabass)',
     '     2: accordionist (accordion)',
     '',
     '     add performers',
     '     delete performers',
     '     move performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> del', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers> 2', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     1: bassist (contrabass)',
     '',
     '     add performers',
     '     delete performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> q', '']
