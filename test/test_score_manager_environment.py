from experimental import *


def test_score_manager_environment_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run('q')

    sekka_menu_line = '     14: Sekka (2007)'
    main_menu_lines = score_manager._session.transcript[0][1]
    assert sekka_menu_line in main_menu_lines
