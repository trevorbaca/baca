from abjad.tools import iotools
import baca


def test_MaterialWrangler_01():
    '''Baca material wrangler.
    '''

    material_wrangler = baca.scf.MaterialWrangler('baca')

    assert material_wrangler.purview.is_studio_global_purview
    
    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.StaticMaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.InteractiveMaterialProxy)

    material_proxies = material_wrangler.iterate_package_proxies()
    #assert all([isinstance(x, baca.scf.MaterialProxy.MaterialProxy) for x in material_proxies])
    assert all([isinstance(x, baca.scf.MaterialProxy) for x in material_proxies])

    names = material_wrangler.iterate_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.iterate_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.iterate_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.iterate_package_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])


def test_MaterialWrangler_02():
    '''Score material wrangler.
    '''

    material_wrangler = baca.scf.MaterialWrangler('manos')

    assert material_wrangler.purview.is_score_local_purview
    
    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.StaticMaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.InteractiveMaterialProxy)

    material_proxies = material_wrangler.iterate_package_proxies()
    #assert all([isinstance(x, baca.scf.MaterialProxy.MaterialProxy) for x in material_proxies])
    assert all([isinstance(x, baca.scf.MaterialProxy) for x in material_proxies])

    names = material_wrangler.iterate_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.iterate_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.iterate_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.iterate_package_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])
