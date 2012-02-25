import scf


def test_InstrumentationEditor_round_trips_01():
    '''Round trip.
    '''
    
    editor = scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 move 1 2 del 2 q')
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
     '     1: accordionist (acc)',
     '     2: bassist (vb)',
     '     3: bassoonist (bsn)',
     '     4: cellist (vc)',
     '     5: clarinetist (B-flat)',
     '     6: flutist (fl)',
     '     7: guitarist (gt)',
     '     8: harpist (hp)',
     '     9: harpsichordist (hpschd)',
     '     10: hornist (hn)',
     '     11: oboist (ob)',
     '     12: percussionist (perc)',
     '     13: pianist (pf)',
     '     14: saxophonist (sax)',
     '     15: trombonist (trb)',
     '     16: trumpeter (tp)',
     '     17: tubist (tb)',
     '     18: violinist (vn)',
     '     19: violist (va)',
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
     '     (1) accordionist: accordion',
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
     '     1: accordionist (acc)',
     '     2: bassist (vb)',
     '     3: bassoonist (bsn)',
     '     4: cellist (vc)',
     '     5: clarinetist (B-flat)',
     '     6: flutist (fl)',
     '     7: guitarist (gt)',
     '     8: harpist (hp)',
     '     9: harpsichordist (hpschd)',
     '     10: hornist (hn)',
     '     11: oboist (ob)',
     '     12: percussionist (perc)',
     '     13: pianist (pf)',
     '     14: saxophonist (sax)',
     '     15: trombonist (trb)',
     '     16: trumpeter (tp)',
     '     17: tubist (tb)',
     '     18: violinist (vn)',
     '     19: violist (va)',
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
     '     (1) accordionist: accordion',
     '     (2) bassist: contrabass',
     '',
     '     add performers',
     '     delete performers',
     '     move performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> move', '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Old number> 1']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['New number> 2']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     (1) bassist: contrabass',
     '     (2) accordionist: accordion',
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
    ['Performers> 2']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['Performers',
     '',
     '     (1) bassist: contrabass',
     '',
     '     add performers',
     '     delete performers',
     '']

    entry_index = entry_index + 1
    assert transcript[entry_index] == \
    ['SCF> q', '']
