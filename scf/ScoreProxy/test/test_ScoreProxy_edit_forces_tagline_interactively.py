# -*- encoding: utf-8 -*-
import baca


def test_ScoreProxy_edit_forces_tagline_interactively_01():

    studio = baca.scf.Studio()
    studio.run(user_input='rec ft for_foo_bar q')
    recursif = baca.scf.ScoreProxy('recursif')
    assert recursif.forces_tagline == 'for foo bar'

    studio.run(user_input='rec ft for_64_pieces_of_percussion q')
    recursif = baca.scf.ScoreProxy('recursif')
    assert recursif.forces_tagline == 'for 64 pieces of percussion'
