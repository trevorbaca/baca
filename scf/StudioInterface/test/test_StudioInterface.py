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
    session = baca.scf.menuing.Session(test='menu_lines')
    studio_interface.work_in_studio(session=session)
    
    assert session.test_result == [  
     'Welcome to the studio.',
     '',
     "     1: L'archipel du corps (2011)",
     '     2: Čáry (2006)',
     '     3: Mon seul désir (2009)',
     "     4: L'imaginare (2010)",
     '     5: Lidércfény (2008)',
     '     6: Las manos mágicas (2011)',
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
    session = baca.scf.menuing.Session(user_input='hidden', test='menu_lines')
    studio_interface.work_in_studio(session=session)

    assert session.test_result == [
     '     all: show mothballed scores',
     '     exec: exec statement',
     '     grep: grep baca directories',
     '     here: edit client source',
     '     hidden: show hidden items',
     '     q: quit',
     '     redraw: redraw',
     '     some: hide mothballed scores',
     '     studio: return to studio',
     '     svn: work with repository',
     '     where: show menu client',
     '']


def test_StudioInterface_04():
    '''Main menu to score menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    session = baca.scf.menuing.Session(user_input='1', test='menu_lines')
    studio_interface.work_in_studio(session=session)

    assert session.test_result == [
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
     '']
