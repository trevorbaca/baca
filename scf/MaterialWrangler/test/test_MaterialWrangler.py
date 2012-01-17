from abjad.tools import iotools
import baca


def test_MaterialWrangler_01():

    material_wrangler = baca.scf.MaterialWrangler()

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.materialproxies.SargassoMeasureMaterialProxy)

    names = material_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.materialproxies.SargassoMeasureMaterialProxy)

    names = material_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])
