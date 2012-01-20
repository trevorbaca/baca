from abjad.tools import iotools
import baca


def test_MaterialPackageWrangler_01():

    material_wrangler = baca.scf.MaterialPackageWrangler()

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialPackageProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker)

    names = material_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])

    material_proxy = material_wrangler.get_package_proxy('baca.materials.sargasso_multipliers')
    assert isinstance(material_proxy, baca.scf.MaterialPackageProxy)

    material_proxy = material_wrangler.get_package_proxy('baca.materials.test_measures_a')
    assert isinstance(material_proxy, baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker)

    names = material_wrangler.list_wrangled_package_importable_names()
    assert all([iotools.is_underscore_delimited_lowercase_package_name(x) for x in names])

    names = material_wrangler.list_wrangled_package_short_names()
    assert all([iotools.is_underscore_delimited_lowercase_string(x) for x in names])

    names = material_wrangler.list_wrangled_package_spaced_names()
    assert all([iotools.is_space_delimited_lowercase_string(x) for x in names])
