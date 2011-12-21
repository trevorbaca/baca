# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
import baca


def test_ScoreProxy_01():
    '''Attributes.
    '''

    score_proxy = baca.scf.ScoreProxy('manos')

    assert isinstance(score_proxy.chunk_wrangler, baca.scf.ChunkWrangler)
    assert isinstance(score_proxy.dist_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.etc_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.exg_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.maker_wrangler, baca.scf.MakerWrangler)
    assert isinstance(score_proxy.material_wrangler, baca.scf.MaterialWrangler)
    assert isinstance(score_proxy.mus_proxy, baca.scf.MusProxy)

    assert score_proxy.has_correct_initializers
    assert score_proxy.is_score_local_purview
    assert not score_proxy.is_studio_global_purview

    instrumentation = scoretools.InstrumentationSpecifier()
    performer_1 = scoretools.Performer('flutist')
    performer_1.instruments.append(instrumenttools.AltoFlute())
    instrumentation.performers.append(performer_1)
    performer_2 = scoretools.Performer('guitarist')
    performer_2.instruments.append(instrumenttools.Guitar())
    instrumentation.performers.append(performer_2)

    assert score_proxy.composer == baca.scf.TrevorBaca()
    assert score_proxy.instrumentation == instrumentation
    assert score_proxy.title == 'Las manos mágicas'
    assert score_proxy.year_of_completion is None

    assert score_proxy.score_initializer_file_names == (
        '/Users/trevorbaca/Documents/scores/manos/__init__.py',
        '/Users/trevorbaca/Documents/scores/manos/mus/__init__.py',
        '/Users/trevorbaca/Documents/scores/manos/mus/chunks/__init__.py',
        '/Users/trevorbaca/Documents/scores/manos/mus/materials/__init__.py')

    assert score_proxy.score_package_wranglers == (
        baca.scf.ChunkWrangler('manos'),
        baca.scf.MaterialWrangler('manos'))    

    assert score_proxy.top_level_subdirectories == (
        baca.scf.DistProxy('manos'),
        baca.scf.EtcProxy('manos'),
        baca.scf.ExgProxy('manos'),
        baca.scf.MusProxy('manos'))


def test_ScoreProxy_02():
    '''Main menu.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.run(user_input='q')

    assert archipel.transcript[-2] == \
    ["L'archipel du corps (2011)",
      '',
      '     Chunks',
      '',
      '     [create chunk] (ch)',
      '',
      '     Materials',
      '',
      '     create interactive material (mi)',
      '     create static material (ms)',
      '',
      '     Setup',
      '',
      '     forces tagline (ft)',
      '     performers (pf)',
      '     title (tl)',
      '     year of completion (yr)',
      '']


def test_ScoreProxy_03():
    '''Main menu to hidden menu.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.run(user_input='hidden q')

    assert archipel.transcript[-2] == [
     '     back',
     '     exec statement',
     '     grep baca directories',
     '     edit client source',
     '     show hidden items',
     '     next score',
     '     prev score',
     '     quit',
     '     redraw',
     '     return to score',
     '     return to studio',
     '     work with repository',
     '     work with tags',
     '     show menu client',
     '']


def test_ScoreProxy_04():
    '''Manage tags menu.
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.session.user_input = 'q'
    archipel.manage_tags()
    assert archipel.ts == (2,)


def test_ScoreProxy_05():
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


def test_ScoreProxy_06():
    '''User 'studio' input results in return to studio main menu.
    '''
    
    studio = baca.scf.Studio()
    studio.run(user_input='1 studio q')

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScoreProxy_07():
    '''User 'studio' input terminates execution (when score not managed from studio).
    '''

    archipel = baca.scf.ScoreProxy('archipel')
    archipel.run(user_input='studio')

    assert len(archipel.transcript) == 2
    assert archipel.transcript[0][0] == "L'archipel du corps (2011)"
    assert archipel.transcript[1][0] == 'SCF> studio'


def test_ScoreProxy_08():
    '''User 'b' input returns to studio main menu.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 b q')

    assert len(studio.transcript) == 6
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScoreProxy_09():
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


def test_ScoreProxy_10():
    '''Back is handled correctly.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 b q')
    transcript = studio.transcript
    
    assert len(transcript) == 6
    assert transcript[0] == transcript[4]
