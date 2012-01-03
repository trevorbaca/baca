from abjad.tools import iotools
import baca


def test_ChunkWrangler_01():
    '''Attributes.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler('manos')
    assert chunk_wrangler.class_name == 'ChunkWrangler'
    assert chunk_wrangler.directory_name == '/Users/trevorbaca/Documents/scores/manos/mus/chunks'
    assert chunk_wrangler.has_directory
    assert chunk_wrangler.has_initializer
    assert chunk_wrangler.initializer_file_name == \
        '/Users/trevorbaca/Documents/scores/manos/mus/chunks/__init__.py'
    assert chunk_wrangler.package_importable_name == 'manos.mus.chunks'
    assert chunk_wrangler.package_short_name == 'chunks'
    assert chunk_wrangler.package_spaced_name == 'chunks'
    assert chunk_wrangler.purview == baca.scf.ScoreProxy('manos')
    assert chunk_wrangler.purview.is_score_local_purview
    assert chunk_wrangler.score == baca.scf.ScoreProxy('manos')
    assert chunk_wrangler.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/ChunkWrangler/ChunkWrangler.py'
    assert chunk_wrangler.spaced_class_name == 'chunk wrangler'
    

def test_ChunkWrangler_02():
    '''Iteration.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler('manos')
    chunk_proxies = chunk_wrangler.iterate_package_proxies()
    assert all([isinstance(x, baca.scf.ChunkProxy) for x in chunk_proxies])

    names = chunk_wrangler.iterate_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = chunk_wrangler.iterate_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = chunk_wrangler.iterate_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = chunk_wrangler.iterate_package_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])


def test_ChunkWrangler_03():
    '''Straightforward methods.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler('manos')

    chunk_proxy = chunk_wrangler.get_package_proxy('manos.mus.chunks.test_chunk')
    assert isinstance(chunk_proxy, baca.scf.ChunkProxy)
