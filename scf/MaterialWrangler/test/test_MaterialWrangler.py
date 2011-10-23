import baca


def test_MaterialWrangler_01():
    '''Baca material wrangler.
    '''

    bmw = baca.scf.MaterialWrangler('baca.materials')
    assert isinstance(bmw.purview, baca.scf.BacaProxy)
    assert not bmw.has_score_local_purview
    assert bmw.has_studio_global_purview
    assert isinstance(bmw.maker_wrangler, baca.scf.MakerWrangler)
    

    
