from abjad.tools import iotools
import baca


def test_MaterialWrangler_01():
    '''Baca material wrangler.
    '''

    material_wrangler = baca.scf.MaterialWrangler('baca')

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxies = material_wrangler.list_package_proxies()
    assert all([isinstance(x, baca.scf.MaterialProxy) for x in material_proxies])

    names = material_wrangler.list_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_package_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])


def test_MaterialWrangler_02():
    '''Score material wrangler.
    '''

    material_wrangler = baca.scf.MaterialWrangler('manos')

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxies = material_wrangler.list_package_proxies()
    assert all([isinstance(x, baca.scf.MaterialProxy) for x in material_proxies])

    names = material_wrangler.list_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_package_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])
