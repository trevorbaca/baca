import baca


def test_ScoreProxy_01():

    score_proxy = baca.scf.ScoreProxy('manos')

    assert isinstance(score_proxy.chunk_wrangler, baca.scf.ChunkWrangler)
    assert isinstance(score_proxy.material_wrangler, baca.scf.MaterialWrangler)
    assert isinstance(score_proxy.maker_wrangler, baca.scf.MakerWrangler)

    # TODO: add asserts for remaining class attributes 
