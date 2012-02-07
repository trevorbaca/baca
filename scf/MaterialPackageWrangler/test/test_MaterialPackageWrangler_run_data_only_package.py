import baca
import py
import types


def test_MaterialPackageWrangler_run_data_only_package_01():
    '''Make data package.
    Delete package.
    '''
    
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input='m d testnumbers default default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert mpp.has_valid_initializer
        assert mpp.has_valid_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
        assert isinstance(baca.materials.testnumbers, types.ModuleType)
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_02():
    '''Make data package. Invalidate initializer.
    Verify invalid initializer. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers incanned canned_exception.py default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert not mpp.has_valid_initializer
        assert mpp.has_valid_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
        assert isinstance(baca.materials.testnumbers, types.ModuleType)
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_03():
    '''Make data package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers incanned canned_exception.py default '
            'inr yes no default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert mpp.has_valid_initializer
        assert mpp.has_valid_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
        assert isinstance(baca.materials.testnumbers, types.ModuleType)
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_04():
    '''Make data package. Create output material.
    Delete package." 
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']
        assert mpp.has_valid_initializer
        assert mpp.has_valid_material_definition_module
        assert mpp.has_valid_output_material_module
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material == [1, 2, 3, 4, 5]
        assert baca.materials.testnumbers == [1, 2, 3, 4, 5]
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_05():
    '''Make data package. Delete material definition module.
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mddelete default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py']
        assert mpp.has_valid_initializer
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
        # TODO: maybe the following line can be made to work?
        # TODO: if Python can be convinced to reread baca.materials?
        #assert isinstance(baca.materials.testnumbers, types.ModuleType)
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_06():
    '''Make data package. Overwrite material definition module with stub.
    Delete package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mdstub default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_07():
    '''Make data package. Copy canned material definition. Make output material. Remove output material.
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default '
            'omdelete default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_08():
    '''Make data package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mdcanned canned_testnumbers_material_definition_with_exception.py default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert mpp.has_valid_initializer
        assert not mpp.has_valid_material_definition_module
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_09():
    '''Make data package. Copy canned material definition module. Make output data. Corrupt output data.
    Verify invalid output material module. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default '
            'omcanned canned_exception.py default q')
        assert studio.package_exists('baca.materials.testnumbers')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']
        assert mpp.has_valid_initializer
        assert mpp.has_valid_material_definition_module
        assert not mpp.has_valid_output_material_module
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('baca.materials.testnumbers')
