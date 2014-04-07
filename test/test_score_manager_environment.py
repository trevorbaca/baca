import scoremanager


def test_score_manager_environment_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'ssv q'
    score_manager._run(pending_user_input=input_)

    assert 'Sekka (2007)' in score_manager._transcript.contents