# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_score_manager_environment_01():

    input_ = 'q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert '5: Chrysanthemums (1995)' in contents
    assert '22: Zeit (1998)' in contents