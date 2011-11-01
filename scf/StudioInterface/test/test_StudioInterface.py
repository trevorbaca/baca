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
    menu_lines = studio_interface.work_in_studio(test = 'menu_lines')
    
    assert menu_lines == [  
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
    '''Hidden menu.
    '''

    studio_interface = baca.scf.StudioInterface()
    menu_lines = studio_interface.work_in_studio(user_input='hidden', test='menu_lines')

    #assert menu_lines == []
