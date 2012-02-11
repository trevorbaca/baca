# -*- encoding: utf-8 -*-
import baca


def test_ScorePackageProxy_edit_title_interactively_01():

    try:
        studio = baca.scf.Studio()
        studio.run(user_input='betorung setup title Foo q')
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Betörung - setup'
        assert studio.transcript[-2][0] == 'Foo - setup'
    finally:
        studio.run(user_input='foo setup title Betörung q')
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Foo - setup'
        assert studio.transcript[-2][0] == 'Betörung - setup'
