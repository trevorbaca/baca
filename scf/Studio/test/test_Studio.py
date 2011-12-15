import baca


def test_Studio_01():
    '''Attributes.
    '''

    studio = baca.scf.Studio()

    assert studio.class_name == 'Studio'
    assert isinstance(studio.global_proxy, baca.scf.GlobalProxy)
    assert isinstance(studio.score_wrangler, baca.scf.ScoreWrangler)
    assert studio.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/Studio/Studio.py'
    assert studio.spaced_class_name == 'studio'


def test_Studio_02():
    '''Main menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='q')
    
    assert studio.transcript[-2] == [  
     'Studio - active scores',
     '',
     "     1: L'archipel du corps (2011)",
     '     2: Betörung (in progress)',
     '     3: Čáry (2006)',
     '     4: Mon seul désir (2009)',
     "     5: L'imaginare (2010)",
     '     6: Lidércfény (2008)',
     '     7: Poème récursif (2005)',
     '     8: Red Shift Hijinks (2005)',
     '     9: Sekka (2007)',
     '',
     '     work with interactive material proxies',
     '     work with Bača materials',
     '']


def test_Studio_03():
    '''Main menu to hidden menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='hidden q')

    assert studio.transcript[-2] == [
     '     show active scores only',   
     '     show all scores',
     '     back',
     '     exec statement',
     '     grep baca directories',
     '     edit client source',
     '     show hidden items',
     '     show mothballed scores only',
     '     next score',
     '     prev score',
     '     quit',
     '     redraw',
     '     return to score',
     '     return to studio',
     '     work with repository',
     '     show menu client',
     '']


def test_Studio_04():
    '''Main menu to score menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 q')

    assert studio.transcript[-2] == [
     "L'archipel du corps (2011)",
     '',
     '     Chunks',
     '',
     '     [create chunk]',
     '',
     '     Materials',
     '',
     '     create interactive material',
     '     create static material',
     '',
     '     Setup',
     '',
     '     performers',
     '']


def test_Studio_05():
    '''Main menu. Mothballed scores only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='mb q')
    
    assert studio.transcript[-2] == [  
     'Studio - mothballed scores',
     '',
     '     1: Arac\xc4\xb1l\xc4\xb1k',
     '     2: Chrysanthemums (1995)',
     '     3: Jivan Mukti',
     '     4: Manifolds',
     '     5: Las manos mágicas',
     '     6: Tack (1996)',
     '     7: Territoires',
     '     8: Zeit (1998)',
     '',
     '     work with interactive material proxies',
     '     work with Bača materials',
     '']


def test_Studio_06():
    '''Main menu to score menu to tags menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 tags q')

    assert studio.transcript[-2] == \
     ["L'archipel du corps (2011) - tags",
      '',
      "     'composer': TrevorBaca()",
      "     'instrumentation': InstrumentationSpecifier([Performer(name='flutist', instruments=[Piccolo(), AltoFlute(), ContrabassFlute(), UntunedPercussion('caxixi', 'cx.')]), Performer(name='guitarist', instruments=[Guitar(), UntunedPercussion('caxixi', 'cx.')]), Performer(name='accordionist', instruments=[Accordion()]), Performer(name='percussionist', instruments=[Marimba(), Glockenspiel(), UntunedPercussion('bass drum', 'b. drum'), UntunedPercussion('claves', 'clv.'), UntunedPercussion('caxixi', 'cx.')])])",
      '     \'title\': "L\'archipel du corps"',
      "     'year_of_completion': 2011",
      '',
      '     add tag',
      '     delete tag',
      '']


def test_Studio_07():
    '''Main menu to svn menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='svn q')

    assert studio.transcript[-2] == [
      'Studio - active scores - repository commands',
      '',
      '     add',
      '     ci',
      '     st',
      '     up',
      '',
      '     add_scores',
      '     ci_scores',
      '     st_scores',
      '     up_scores',
      '',
      '     pytest',
      '     pytest_scores',
      '     pytest_all',
      '']


def test_Studio_08():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='q')
    assert studio.transcript[-2][0] == 'Studio - active scores'

    studio.run(user_input='svn q')
    assert studio.transcript[-2][0] == 'Studio - active scores - repository commands'

    studio.run(user_input='svn b q')
    assert studio.transcript[-2][0] == 'Studio - active scores'


def test_Studio_09():
    '''Junk works.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='foo q')
    assert len(studio.transcript) == 4

    studio.run(user_input='foo bar q')
    assert len(studio.transcript) == 6


# TODO: combine studio, junk, back, score tests into a single case
def test_Studio_10():
    '''User 'studio' input results in (dummy) redraw of studio main menu.
    '''
    
    studio = baca.scf.Studio()
    studio.run(user_input='foo q')
    assert len(studio.transcript) == 4

    menu_0 = studio.transcript[0]
    menu_2 = studio.transcript[2]
    assert menu_0 == menu_2


def test_Studio_11():
    '''Back is handled correctly.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='foo q')
    assert len(studio.transcript) == 4

    menu_0 = studio.transcript[0]
    menu_2 = studio.transcript[2]
    assert menu_0 == menu_2


def test_Studio_12():
    '''Exec works.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='exec 2**30 q')

    assert len(studio.transcript) == 5
    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> 2**30', '']
    assert studio.transcript[3] == ['1073741824', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_13():
    '''Exec protects against senseless input.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='exec foo q')

    assert len(studio.transcript) == 5
    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> foo', '']
    assert studio.transcript[3] == ['Expression not executable.', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_14():
    '''Shared session.
    '''

    studio = baca.scf.Studio()

    assert studio.session is studio.global_proxy.session
    assert studio.session is studio.score_wrangler.session


def test_Studio_15():
    '''Display string navigation.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='Mon b desir b q')
    assert studio.ts == (10, (0, 4, 8), (2, 6), (3, 7))


def test_Studio_16():
    '''Backtracking stu* shortcut.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='desir perf studio q')
    ts_1 = studio.ts

    studio = baca.scf.Studio()
    studio.run(user_input='desir perf stu q')
    ts_2 = studio.ts
    
    assert ts_1 == ts_2


def test_Studio_17():
    '''Backtracking sco* shortcut.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='desir perf score q')
    ts_1 = studio.ts

    studio = baca.scf.Studio()
    studio.run(user_input='desir perf sco q')
    ts_2 = studio.ts
    
    assert ts_1 == ts_2
