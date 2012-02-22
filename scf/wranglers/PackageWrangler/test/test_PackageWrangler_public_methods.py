import baca


def test_PackageWrangler_public_methods_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    wrangler_2 = wrangler.get_asset_proxy('scf')
    assert isinstance(wrangler_2, baca.scf.proxies.PackageProxy)

    assert 'lidercfeny' in wrangler.list_asset_importable_names()
    assert ('lidercfeny', 'lidercfeny') in wrangler.list_visible_asset_menuing_pairs()
   
    lidercfeny = baca.scf.proxies.PackageProxy('lidercfeny')
    assert lidercfeny in wrangler.list_asset_proxies()

    assert wrangler.list_asset_proxies() == wrangler.list_visible_asset_proxies()
    assert 'lidercfeny' in wrangler.list_asset_short_names()
    assert 'lidercfeny' in wrangler.list_asset_human_readable_names()
