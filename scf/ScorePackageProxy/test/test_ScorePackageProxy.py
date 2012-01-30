# -*- encoding: utf-8 -*-
import baca


def test_ScorePackageProxy_01():
    '''Main menu.
    '''

    archipel = baca.scf.ScorePackageProxy('archipel')
    archipel.run(user_input='q')

    assert archipel.transcript[-2] == \
    ["L'archipel du corps (2011)",
      '',
      '     chunks (h)',
      '     materials (m)',
      '',
      '     forces tagline (ft)',
      '     performers (pf)',
      '     title (tl)',
      '     year of completion (yr)',
      '']


def test_ScorePackageProxy_02():
    '''Manage tags menu.
    '''

    archipel = baca.scf.ScorePackageProxy('archipel')
    archipel.session.user_input = 'q'
    archipel.manage_tags()
    assert archipel.ts == (2,)


def test_ScorePackageProxy_03():
    '''Add and delete tag interactively.
    '''

    archipel = baca.scf.ScorePackageProxy('archipel')
    archipel.session.user_input = 'add foo bar q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') == 'bar'

    archipel = baca.scf.ScorePackageProxy('archipel')
    archipel.session.user_input = 'del foo q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') is None


def test_ScorePackageProxy_04():
    '''User 'studio' input results in return to studio main menu.
    '''
    
    studio = baca.scf.Studio()
    studio.run(user_input="l'arch studio q")

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_05():
    '''User 'studio' input terminates execution (when score not managed from studio).
    '''

    archipel = baca.scf.ScorePackageProxy('archipel')
    archipel.run(user_input='studio')

    assert len(archipel.transcript) == 2
    assert archipel.transcript[0][0] == "L'archipel du corps (2011)"
    assert archipel.transcript[1][0] == 'SCF> studio'


def test_ScorePackageProxy_06():
    '''User 'b' input returns to studio main menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input="l'arch b q")

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_07():
    '''Shared session.
    '''

    spp = baca.scf.ScorePackageProxy('archipel')

    assert spp.session is spp.dist_proxy.session
    assert spp.session is spp.etc_proxy.session
    assert spp.session is spp.exg_proxy.session
    assert spp.session is spp.mus_proxy.session
    assert spp.session is spp.chunk_wrangler.session
    assert spp.session is spp.material_wrangler.session
    assert spp.session is spp.material_package_maker_wrangler.session


def test_ScorePackageProxy_08():
    '''Back is handled correctly.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input="l'arch b q")
    transcript = studio.transcript
    
    assert len(transcript) == 6
    assert transcript[0] == transcript[4]
