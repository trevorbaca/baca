import baca


def test_StudioInterface_01():
    '''Attributes.
    '''

    studio_interface = baca.scf.StudioInterface()

    assert studio_interface.class_name == 'StudioInterface'
    assert isinstance(studio_interface.global_proxy, baca.scf.GlobalProxy)
    assert isinstance(studio_interface.score_wrangler, baca.scf.ScoreWrangler)
    assert studio_interface.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/StudioInterface/StudioInterface.py'
    assert studio_interface.spaced_class_name == 'studio interface'


def test_StudioInterface_02():
    '''Main menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.work_in_studio()
    
    assert studio_interface.session.test_result == [  
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


def test_StudioInterface_03():
    '''Main menu to hidden menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = 'hidden'
    studio_interface.work_in_studio()

    assert studio_interface.session.test_result == [
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


def test_StudioInterface_04():
    '''Main menu to score menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = '1'
    studio_interface.work_in_studio()

    assert studio_interface.session.test_result == [
     "L'archipel du corps",
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
     '     instr: edit instrumentation',
     '']


def test_StudioInterface_05():
    '''Main menu. Mothballed scores only.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = 'mb'
    studio_interface.work_in_studio()
    
    assert studio_interface.session.test_result == [  
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


def test_StudioInterface_06():
    '''Main menu to score menu to tags menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = '1\ntags'
    studio_interface.work_in_studio()

    assert studio_interface.session.test_result == [
     "L'archipel du corps - tags",
     '',
     "     'composer': TrevorBaca()",
     '     \'title\': "L\'archipel du corps"',
     "     'year_of_completion': 2011",
     '',
     '     add: add tag',
     '     del: delete tag',
     '']


def test_StudioInterface_07():
    '''Main menu to svn menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = 'svn'
    studio_interface.work_in_studio()

    assert studio_interface.session.test_result == [
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


def test_StudioInterface_08():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = ''
    studio_interface.work_in_studio()
    assert studio_interface.session.test_result[0] == 'Studio - active scores'

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = 'svn'
    studio_interface.work_in_studio()
    assert studio_interface.session.test_result[0] == 'Studio - active scores - repository commands'

    studio_interface = baca.scf.StudioInterface()
    studio_interface.session.test = 'menu_lines'
    studio_interface.session.user_input = 'svn\nb'
    studio_interface.work_in_studio()
    assert studio_interface.session.test_result[0] == 'Studio - active scores'


def test_StudioInterface_09():
    '''Changing from main menu to svn menu raises no exceptions and stops execution when finished.
    '''

    session = baca.scf.Session(user_input='svn')
    studio_interface = baca.scf.StudioInterface(session=session)
    studio_interface.work_in_studio()
