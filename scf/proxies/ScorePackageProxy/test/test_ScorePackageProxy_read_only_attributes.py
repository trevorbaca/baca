# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
import baca


def test_ScorePackageProxy_read_only_attributes_01():
    '''Read-only public attributes.
    '''

    score_proxy = baca.scf.proxies.ScorePackageProxy('manos')


    assert isinstance(score_proxy.chunk_wrangler, baca.scf.wranglers.ChunkPackageWrangler)
    assert isinstance(score_proxy.dist_proxy, baca.scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.etc_proxy, baca.scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.exg_proxy, baca.scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.material_package_maker_wrangler, baca.scf.wranglers.MaterialPackageMakerWrangler)
    assert isinstance(score_proxy.material_package_wrangler, baca.scf.wranglers.MaterialPackageWrangler)
    assert isinstance(score_proxy.mus_proxy, baca.scf.proxies.MusPackageProxy)

    assert score_proxy.has_correct_initializers

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
        baca.scf.wranglers.ChunkPackageWrangler(),
        baca.scf.wranglers.MaterialPackageWrangler())    

    assert score_proxy.top_level_directory_proxies == (
        baca.scf.proxies.DistDirectoryProxy('manos'),
        baca.scf.proxies.EtcDirectoryProxy('manos'),
        baca.scf.proxies.ExgDirectoryProxy('manos'),
        baca.scf.proxies.MusPackageProxy('manos'))
