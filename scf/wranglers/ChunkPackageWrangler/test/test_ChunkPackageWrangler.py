from abjad.tools import iotools
import baca


def test_ChunkPackageWrangler_01():
    '''Attributes.
    '''

    chunk_wrangler = baca.scf.wranglers.ChunkPackageWrangler()
    assert chunk_wrangler.class_name == 'ChunkPackageWrangler'
    assert chunk_wrangler.score_internal_wrangler_target_package_importable_name_suffix == 'mus.chunks'
    assert chunk_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/wranglers/ChunkPackageWrangler/ChunkPackageWrangler.py'
    assert chunk_wrangler.spaced_class_name == 'chunk package wrangler'
    

def test_ChunkPackageWrangler_02():
    '''Iteration.
    '''

    chunk_wrangler = baca.scf.wranglers.ChunkPackageWrangler()

    names = chunk_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = chunk_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = chunk_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])


def test_ChunkPackageWrangler_03():
    '''Straightforward methods.
    '''

    chunk_wrangler = baca.scf.wranglers.ChunkPackageWrangler()

    chunk_proxy = chunk_wrangler.get_package_proxy('manos.mus.chunks.test_chunk')
    assert isinstance(chunk_proxy, baca.scf.proxies.ChunkPackageProxy)
