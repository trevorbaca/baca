from abjad.tools import iotools
import baca


def test_MaterialWrangler_01():
    '''Baca material wrangler.
    '''

    material_wrangler = baca.scf.MaterialWrangler('baca.materials')

    assert material_wrangler.purview.is_studio_global_purview
    assert issubclass(material_wrangler.InteractiveMaterialProxy, baca.scf.InteractiveMaterialProxy)
    assert issubclass(material_wrangler.StaticMaterialProxy, baca.scf.StaticMaterialProxy)
    
    material_proxy = material_wrangler.get_material_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.StaticMaterialProxy)

    material_proxy = material_wrangler.get_material_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.InteractiveMaterialProxy)

    material_proxies = material_wrangler.iterate_material_proxies()
    assert all([isinstance(x, baca.scf._MaterialProxy._MaterialProxy) for x in material_proxies])

    names = material_wrangler.list_material_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_material_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_material_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_material_underscored_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])
