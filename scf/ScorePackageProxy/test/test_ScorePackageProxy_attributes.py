# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
import baca


def test_ScorePackageProxy_attributes_01():
    '''Read-only public attributes.
    '''

    score_proxy = baca.scf.ScorePackageProxy('manos')


    assert isinstance(score_proxy.chunk_wrangler, baca.scf.ChunkPackageWrangler)
    assert isinstance(score_proxy.dist_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.etc_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.exg_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.material_proxy_wrangler, baca.scf.MaterialPackageMakerWrangler)
    assert isinstance(score_proxy.material_wrangler, baca.scf.MaterialPackageWrangler)
    assert isinstance(score_proxy.mus_proxy, baca.scf.MusPackageProxy)

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

    assert score_proxy.annotated_title == 'Las manos mágicas'
    assert score_proxy.breadcrumb == 'Las manos mágicas'
    assert score_proxy.composer == 'Trevor Bača'
    assert score_proxy.instrumentation == instrumentation
    assert score_proxy.materials_package_importable_name == 'manos.mus.materials'
    assert score_proxy.title == 'Las manos mágicas'
    assert score_proxy.year_of_completion is None

    assert score_proxy.score_initializer_file_names == (
        '/Users/trevorbaca/Documents/scores/manos/__init__.py',
        '/Users/trevorbaca/Documents/scores/manos/mus/__init__.py',)

    assert score_proxy.score_package_wranglers == (
        baca.scf.ChunkPackageWrangler(),
        baca.scf.MaterialPackageWrangler())    

    assert score_proxy.top_level_subdirectories == (
        baca.scf.DistDirectoryProxy('manos'),
        baca.scf.EtcDirectoryProxy('manos'),
        baca.scf.ExgDirectoryProxy('manos'),
        baca.scf.MusPackageProxy('manos'))
