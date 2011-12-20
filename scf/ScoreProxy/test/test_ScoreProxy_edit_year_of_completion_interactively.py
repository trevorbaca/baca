# -*- encoding: utf-8 -*-
import baca


def test_ScoreProxy_edit_year_of_completion_interactively_01():

    studio = baca.scf.Studio()
    studio.run(user_input='arch yr 2001 q')
    assert studio.ts == (7,)
    assert studio.transcript[-5][0] == "L'archipel du corps (2011)"
    assert studio.transcript[-2][0] == "L'archipel du corps (2001)"

    studio.run(user_input='arch yr 2011 q')
    assert studio.ts == (7,)
    assert studio.transcript[-5][0] == "L'archipel du corps (2001)"
    assert studio.transcript[-2][0] == "L'archipel du corps (2011)"
