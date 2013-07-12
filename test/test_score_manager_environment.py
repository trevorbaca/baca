from experimental import *


def test_score_manager_environment_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run('q')

    main_menu_lines = score_manager._session.io_transcript[0][1]
    sekka_menu_line_without_number = 'Sekka (2007)'
    for line in main_menu_lines:
        if sekka_menu_line_without_number in line:
            break
    else:
        raise Exception('Sekka not found.')
