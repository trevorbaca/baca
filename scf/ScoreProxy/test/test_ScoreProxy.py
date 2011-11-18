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

    # FIXME
    #assert score_proxy.has_correct_directory_structure
    assert score_proxy.has_correct_initializers
    #assert score_proxy.has_correct_package_structure

    assert score_proxy.is_score_local_purview
    assert not score_proxy.is_studio_global_purview

    instrumentation = scoretools.InstrumentationSpecifierEditor()
    performer_1 = scoretools.Performer('Alto Flute')
    performer_1.instruments.append(instrumenttools.AltoFlute())
    instrumentation.performers.append(performer_1)
    performer_2 = scoretools.Performer('Guitar')
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

    session = baca.scf.menuing.Session(test='menu_lines')
    archipel = baca.scf.ScoreProxy('archipel', session=session)
    archipel.manage_score()

    assert session.test_result == [
     "L'archipel du corps",
     '',
     '     Chunks',
     '',
     '     ch: [create chunk]',
     '',
     '     Materials',
     '',
     '     mi: create interactive material',
     '     ms: create static material',
     '',
     '     Setup',
     '',
     '     instr: edit instrumentation',
     '']


def test_ScoreProxy_03():
    '''Main menu to hidden menu.
    '''

    session = baca.scf.menuing.Session(user_input='hidden', test='menu_lines')
    archipel = baca.scf.ScoreProxy('archipel', session=session)
    archipel.manage_score()

    assert session.test_result == [
     '     b: back',
     '     exec: exec statement',
     '     grep: grep baca directories',
     '     here: edit client source',
     '     hidden: show hidden items',
     '     q: quit',
     '     redraw: redraw',
     '     studio: return to studio',
     '     svn: work with repository',
     '     tags: work with tags',
     '     where: show menu client',
     '']


def test_ScoreProxy_04():
    '''Manage tags menu.
    '''

    session = baca.scf.menuing.Session(test='menu_lines')
    archipel = baca.scf.ScoreProxy('archipel', session=session)
    archipel.manage_tags()

    assert session.test_result == [
     'Tags',
     '',
     "     'composer': TrevorBaca()",
     '     \'title\': "L\'archipel du corps"',
     "     'year_of_completion': 2011",
     '',
     '     add: add tag',
     '     del: delete tag',
     '']


def test_ScoreProxy_05():
    '''Add and delete tag interactively.
    '''

    session = baca.scf.menuing.Session(user_input="add\nfoo\nbar")
    archipel = baca.scf.ScoreProxy('archipel', session=session)
    archipel.manage_tags()
    assert archipel.get_tag('foo') == 'bar'

    session = baca.scf.menuing.Session(user_input="del\nfoo")
    archipel = baca.scf.ScoreProxy('archipel', session=session)
    archipel.manage_tags()
    assert archipel.get_tag('foo') is None
