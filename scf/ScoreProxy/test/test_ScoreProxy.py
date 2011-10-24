import baca


def test_ScoreProxy_01():

    score_proxy = baca.scf.ScoreProxy('manos')

    assert isinstance(score_proxy.chunk_wrangler, baca.scf.ChunkWrangler)
    assert isinstance(score_proxy.dist_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.etc_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.exg_proxy, baca.scf.DirectoryProxy)
    assert isinstance(score_proxy.maker_wrangler, baca.scf.MakerWrangler)
    assert isinstance(score_proxy.material_wrangler, baca.scf.MaterialWrangler)

    assert score_proxy.has_correct_directory_structure
    assert score_proxy.has_correct_initializers
    assert score_proxy.has_correct_package_structure

    assert score_proxy.is_score_local_purview
    assert not score_proxy.is_studio_global_purview

    assert score_proxy.score_composer == 'Trevor Bača'
