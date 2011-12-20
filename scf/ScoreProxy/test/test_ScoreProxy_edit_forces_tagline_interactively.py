# -*- encoding: utf-8 -*-
import baca


def test_ScoreProxy_edit_forces_tagline_interactively_01():
    '''Quit, back, score & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 ft q')
    assert studio.ts == (5,)

    studio.run(user_input='1 ft b q')
    assert studio.ts == (7, (2, 5))

    studio.run(user_input='1 ft sco q')
    assert studio.ts == (7, (2, 5))

    studio.run(user_input='1 ft stu q')
    assert studio.ts == (7, (0, 5))


def test_ScoreProxy_edit_forces_tagline_interactively_02():

    studio = baca.scf.Studio()
    studio.run(user_input='rec ft for_foo_bar q')
    recursif = baca.scf.ScoreProxy('recursif')
    assert recursif.forces_tagline == 'for foo bar'

    studio.run(user_input='rec ft for_64_pieces_of_percussion q')
    recursif = baca.scf.ScoreProxy('recursif')
    assert recursif.forces_tagline == 'for 64 pieces of percussion'
