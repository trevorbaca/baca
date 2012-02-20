import baca


def test_PackageWrangler_public_methods_01():

    wrangler = baca.scf.wranglers.PackageWrangler()

    wrangler_2 = wrangler.get_wrangled_package_proxy('scf')
    assert isinstance(wrangler_2, baca.scf.proxies.PackageProxy)

    assert 'lidercfeny' in wrangler.list_wrangled_package_importable_names()
    assert ('lidercfeny', 'lidercfeny') in wrangler.list_wrangled_package_menuing_pairs()
   
    lidercfeny = baca.scf.proxies.PackageProxy('lidercfeny')
    assert lidercfeny in wrangler.list_wrangled_package_proxies()

    assert wrangler.list_wrangled_package_proxies() == wrangler.list_visible_wrangled_package_proxies()
    assert 'lidercfeny' in wrangler.list_wrangled_package_short_names()
    assert 'lidercfeny' in wrangler.list_wrangled_package_spaced_names()
