# -*- encoding: utf-8 -*-
import baca


def test_ScoreProxy_edit_title_interactively_01():

    studio = baca.scf.Studio()
    studio.run(user_input='bet title Foo q')
    assert studio.ts == (7,)
    assert studio.transcript[-5][0] == 'Betörung'
    assert studio.transcript[-2][0] == 'Foo'

    studio.run(user_input='bet title Betörung q')
    assert studio.ts == (7,)
    assert studio.transcript[-5][0] == 'Foo'
    assert studio.transcript[-2][0] == 'Betörung'
