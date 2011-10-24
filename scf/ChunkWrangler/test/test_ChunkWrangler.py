from abjad.tools import iotools
import baca


def test_ChunkWrangler_01():

    chunk_wrangler = baca.scf.ChunkWrangler('manos')

    assert chunk_wrangler.purview.is_score_local_purview
    assert issubclass(chunk_wrangler.ChunkProxy, baca.scf.ChunkProxy)
    
    # TODO: uncomment when Manos chunks exist
    #chunk_proxy = chunk_wrangler.get_package_proxy('manos.chunks.foo')
    #assert isinstance(chunk_proxy, baca.scf.ChunkProxy)

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
