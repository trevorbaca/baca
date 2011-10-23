import baca


def test_MaterialWrangler_01():
    '''Baca material wrangler.
    '''

    bmw = baca.scf.MaterialWrangler('baca.materials')
    assert bmw.purview.is_studio_global_purview
    assert isinstance(bmw.maker_wrangler, baca.scf.MakerWrangler)
