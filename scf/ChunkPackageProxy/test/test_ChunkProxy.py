import baca


def test_ChunkPackageProxy_01():

    chunk_proxy = baca.scf.ChunkPackageProxy('manos.mus.chunks.test_chunk')

    assert chunk_proxy.class_name == 'ChunkPackageProxy'
    assert chunk_proxy.initializer_file_name == \
        '/Users/trevorbaca/Documents/scores/manos/mus/chunks/test_chunk/__init__.py'
    assert chunk_proxy.package_importable_name == 'manos.mus.chunks.test_chunk'
    assert chunk_proxy.purview == baca.scf.ScoreProxy('manos')
    assert chunk_proxy.score == baca.scf.ScoreProxy('manos')
    assert chunk_proxy.score_template is None
    assert chunk_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/ChunkPackageProxy/ChunkPackageProxy.py'
    assert chunk_proxy.spaced_class_name == 'chunk package proxy'

    assert not chunk_proxy.has_initializer
