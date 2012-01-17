from abjad.tools import iotools
import baca


def test_ChunkWrangler_01():
    '''Attributes.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler()
    assert chunk_wrangler.class_name == 'ChunkWrangler'
    assert chunk_wrangler.toplevel_score_package_importable_name_body == 'mus.chunks'
    assert chunk_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/ChunkWrangler/ChunkWrangler.py'
    assert chunk_wrangler.spaced_class_name == 'chunk wrangler'
    

def test_ChunkWrangler_02():
    '''Iteration.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler()

    names = chunk_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = chunk_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = chunk_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])


def test_ChunkWrangler_03():
    '''Straightforward methods.
    '''

    chunk_wrangler = baca.scf.ChunkWrangler()

    chunk_proxy = chunk_wrangler.get_package_proxy('manos.mus.chunks.test_chunk')
    assert isinstance(chunk_proxy, baca.scf.ChunkProxy)
