# -*- encoding: utf-8 -*-
import baca


def test_ScoreProxy_01():
    '''Main menu.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.run(user_input='q')

#    assert archipel.transcript[-2] == \
#    ["L'archipel du corps (2011)",
#      '',
#      '     Chunks',
#      '',
#      '     [create chunk] (ch)',
#      '',
#      '     Materials',
#      '',
#      '     create interactive material (mi)',
#      '     create static material (ms)',
#      '',
#      '     Setup',
#      '',
#      '     forces tagline (ft)',
#      '     performers (pf)',
#      '     title (tl)',
#      '     year of completion (yr)',
#      '']


def test_ScoreProxy_02():
    '''Manage tags menu.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.session.user_input = 'q'
    archipel.manage_tags()
    assert archipel.ts == (2,)


def test_ScoreProxy_03():
    '''Add and delete tag interactively.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.session.user_input = 'add foo bar q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') == 'bar'

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.session.user_input = 'del foo q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') is None


def test_ScoreProxy_04():
    '''User 'studio' input results in return to studio main menu.
    '''
    
    studio = baca.scf.Studio()
    studio.run(user_input='1 studio q')

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScoreProxy_05():
    '''User 'studio' input terminates execution (when score not managed from studio).
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.run(user_input='studio')

    assert len(archipel.transcript) == 2
    assert archipel.transcript[0][0] == "L'archipel du corps (2011)"
    assert archipel.transcript[1][0] == 'SCF> studio'


def test_ScoreProxy_06():
    '''User 'b' input returns to studio main menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 b q')

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScoreProxy_07():
    '''Shared session.
    '''

    score_proxy = baca.scf.ScoreProxy('archipel')

    assert score_proxy.session is score_proxy.dist_proxy.session
    assert score_proxy.session is score_proxy.etc_proxy.session
    assert score_proxy.session is score_proxy.exg_proxy.session
    assert score_proxy.session is score_proxy.mus_proxy.session
    assert score_proxy.session is score_proxy.chunk_wrangler.session
    assert score_proxy.session is score_proxy.material_wrangler.session
    assert score_proxy.session is score_proxy.maker_wrangler.session


def test_ScoreProxy_08():
    '''Back is handled correctly.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 b q')
    transcript = studio.transcript
    
    assert len(transcript) == 6
    assert transcript[0] == transcript[4]
