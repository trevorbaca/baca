import baca


def test_InstrumentationEditor_round_trips_01():
    '''Round trip.
    '''
    
    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 mv 1 2 del 2 q')
    assert editor.transcript == \
    [['Performers & instrumentation', '', '     add: add performer', ''],
     ['SCF> add', ''],
     ['Performers & instrumentation - add performer',
      '',
      '     1: accordionist',
      '     2: bassist',
      '     3: bassoonist',
      '     4: cellist',
      '     5: clarinetist',
      '     6: flutist',
      '     7: guitarist',
      '     8: harpist',
      '     9: hornist',
      '     10: oboist',
      '     11: percussionist',
      '     12: pianist',
      '     13: trombonist',
      '     14: trumpeter',
      '     15: tuba player',
      '     16: vibraphonist',
      '     17: violinist',
      '     18: violist',
      '     19: xylophonist',
      ''],
     ['SCF> 1', ''],
     ['Performers & instrumentation - add performer - accordionist',
      '',
      '     Select instrument',
      '',
      '     1: accordion',
      '',
      '     other: other instruments',
      '     none: no instruments',
      ''],
     ['SCF> 1', ''],
     ['Performers & instrumentation',
      '',
      '     Performers',
      '',
      '     1: accordionist (accordion)',
      '',
      '     add: add performer',
      '     del: delete performer',
      ''],
     ['SCF> add', ''],
     ['Performers & instrumentation - add performer',
      '',
      '     1: accordionist',
      '     2: bassist',
      '     3: bassoonist',
      '     4: cellist',
      '     5: clarinetist',
      '     6: flutist',
      '     7: guitarist',
      '     8: harpist',
      '     9: hornist',
      '     10: oboist',
      '     11: percussionist',
      '     12: pianist',
      '     13: trombonist',
      '     14: trumpeter',
      '     15: tuba player',
      '     16: vibraphonist',
      '     17: violinist',
      '     18: violist',
      '     19: xylophonist',
      ''],
     ['SCF> 2', ''],
     ['Performers & instrumentation - add performer - bassist',
      '',
      '     Select instrument',
      '',
      '     1: contrabass',
      '',
      '     other: other instruments',
      '     none: no instruments',
      ''],
     ['SCF> 1', ''],
     ['Performers & instrumentation',
      '',
      '     Performers',
      '',
      '     1: accordionist (accordion)',
      '     2: bassist (contrabass)',
      '',
      '     add: add performer',
      '     del: delete performer',
      '     mv: move performer',
      ''],
     ['SCF> mv', ''],
     ['Old number> 1', ''],
     ['New number> 2', ''],
     ['Performers & instrumentation',
      '',
      '     Performers',
      '',
      '     1: bassist (contrabass)',
      '     2: accordionist (accordion)',
      '',
      '     add: add performer',
      '     del: delete performer',
      '     mv: move performer',
      ''],
     ['SCF> del', ''],
     ['Performer number> 2', ''],
     ['Performers & instrumentation',
      '',
      '     Performers',
      '',
      '     1: bassist (contrabass)',
      '',
      '     add: add performer',
      '     del: delete performer',
      ''],
     ['SCF> q', '']]
