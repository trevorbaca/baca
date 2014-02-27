import scoremanager


def test_score_manager_environment_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run('q', display_active_scores=True)

    lines = score_manager._transcript.entries[0].lines
    for line in lines:
        if 'Sekka (2007)' in line:
            break
    else:
        raise Exception('Sekka not found.')
