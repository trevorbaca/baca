import scf


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scf.wranglers.MaterialPackageWrangler()
    assert not wrangler.package_exists('materials.testnumbers')

    try:
        wrangler.make_data_package('materials.testnumbers')
        assert wrangler.package_exists('materials.testnumbers')
        mpp = scf.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.package_exists('materials.testnumbers')
