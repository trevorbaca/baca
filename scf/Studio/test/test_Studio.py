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
    studio.session.user_input = 'q'
    studio.run()
    
    assert studio.session.transcript[-2] == [  
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
     '     k: work with interactive material proxies',
     '     m: work with Bača materials',
     '']


def test_Studio_03():
    '''Main menu to hidden menu.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'hidden q'
    studio.run()

    assert studio.session.transcript[-2] == [
     '     active: show active scores only',   
     '     all: show all scores',
     '     exec: exec statement',
     '     grep: grep baca directories',
     '     here: edit client source',
     '     hidden: show hidden items',
     '     mb: show mothballed scores only',
     '     q: quit',
     '     redraw: redraw',
     '     studio: return to studio',
     '     svn: work with repository',
     '     where: show menu client',
     '']


def test_Studio_04():
    '''Main menu to score menu.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 q'
    studio.run()

    assert studio.session.transcript[-2] == [
     "L'archipel du corps (2011)",
     '',
     '     Chunks',
     '',
     '     ch: [create chunk]',
     '',
     '     Materials',
     '',
     '     mi: create interactive material',
     '     ms: create static material',
     '',
     '     Setup',
     '',
     '     perf: performers & instrumentation',
     '']


def test_Studio_05():
    '''Main menu. Mothballed scores only.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'mb q'
    studio.run()
    
    assert studio.session.transcript[-2] == [  
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
     '     k: work with interactive material proxies',
     '     m: work with Bača materials',
     '']


def test_Studio_06():
    '''Main menu to score menu to tags menu.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = '1 tags q'
    studio.run()

    assert studio.session.transcript[-2] == \
     ["L'archipel du corps (2011) - tags",
      '',
      "     'composer': TrevorBaca()",
      "     'instrumentation': InstrumentationSpecifier([Performer(name='flutist', instruments=[Piccolo(), AltoFlute(), ContrabassFlute(), UntunedPercussion('caxixi', 'cx.')]), Performer(name='guitarist', instruments=[Guitar(), UntunedPercussion('caxixi', 'cx.')]), Performer(name='accordionist', instruments=[Accordion()]), Performer(name='percussionist', instruments=[Marimba(), Glockenspiel(), UntunedPercussion('bass drum', 'b. drum'), UntunedPercussion('claves', 'clv.'), UntunedPercussion('caxixi', 'cx.')])])",
      '     \'title\': "L\'archipel du corps"',
      "     'year_of_completion': 2011",
      '',
      '     add: add tag',
      '     del: delete tag',
      '']


def test_Studio_07():
    '''Main menu to svn menu.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'svn q'
    studio.run()

    assert studio.session.transcript[-2] == [
     'Studio - active scores - repository commands',
     '',
     '     add: svn add',
     '     ci: svn commit',
     '     st: svn status',
     '     up: svn update',
     '',
     '     add scores: svn add (scores)',
     '     ci scores: svn commit (scores)',
     '     st scores: svn status (scores)',
     '     up scores: svn update (scores)',
     '',
     '     pytest: run regression tests',
     '     pytest scores: run regression tests (scores)',
     '     pytest all: run regression tests (all)',
     '']


def test_Studio_08():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'q'
    studio.run()
    assert studio.session.transcript[-2][0] == 'Studio - active scores'

    studio = baca.scf.Studio()
    studio.session.user_input = 'svn q'
    studio.run()
    assert studio.session.transcript[-2][0] == 'Studio - active scores - repository commands'

    studio = baca.scf.Studio()
    studio.session.user_input = 'svn b q'
    studio.run()
    assert studio.session.transcript[-2][0] == 'Studio - active scores'


def test_Studio_09():
    '''Junk works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'foo q'
    studio.run()
    assert len(studio.session.transcript) == 4

    studio = baca.scf.Studio()
    studio.session.user_input = 'foo bar q'
    studio.run()
    assert len(studio.session.transcript) == 6


def test_Studio_10():
    '''User 'studio' input results in (dummy) redraw of studio main menu.
    '''
    
    studio = baca.scf.Studio()
    studio.session.user_input = 'foo q'
    studio.run()
    assert len(studio.session.transcript) == 4

    menu_0 = studio.session.transcript[0]
    menu_2 = studio.session.transcript[2]
    assert menu_0 == menu_2


def test_Studio_11():
    '''Back is handled correctly.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'foo q'
    studio.run()
    assert len(studio.session.transcript) == 4

    menu_0 = studio.session.transcript[0]
    menu_2 = studio.session.transcript[2]
    assert menu_0 == menu_2


def test_Studio_12():
    '''Exec works.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'exec 2**30 q'
    studio.run()

    assert len(studio.session.transcript) == 5
    assert studio.session.transcript[1] == ['SCF> exec', '']
    assert studio.session.transcript[2] == ['XCF> 2**30', '']
    assert studio.session.transcript[3] == ['1073741824', '']
    assert studio.session.transcript[4] == ['SCF> q', '']


def test_Studio_13():
    '''Exec protects against senseless input.
    '''

    studio = baca.scf.Studio()
    studio.session.user_input = 'exec foo q'
    studio.run()

    assert len(studio.session.transcript) == 5
    assert studio.session.transcript[1] == ['SCF> exec', '']
    assert studio.session.transcript[2] == ['XCF> foo', '']
    assert studio.session.transcript[3] == ['Expression not executable.', '']
    assert studio.session.transcript[4] == ['SCF> q', '']


def test_Studio_14():
    '''Shared session.
    '''

    studio = baca.scf.Studio()

    assert studio.session is studio.global_proxy.session
    assert studio.session is studio.score_wrangler.session
