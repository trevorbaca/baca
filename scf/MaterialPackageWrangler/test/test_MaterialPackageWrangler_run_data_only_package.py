import baca
import py


def test_MaterialPackageWrangler_run_data_only_package_01():
    '''Make data package.
    Delete package.
    '''
    
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input='m d testdata default default q')
        assert studio.package_exists('baca.materials.testdata')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_data_only_package_02():
    '''Make data package. Create output material.
    Delete package." 
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input=
            'm d testdata default default '
            'testdata mdcanned canned_testdata_material_definition.py default '
            'dc default q')
        assert studio.package_exists('baca.materials.testdata')
        assert baca.materials.testdata == [1, 2, 3, 4, 5]
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']
        assert mpp.has_material_definition
        assert mpp.has_material_definition_module
        assert mpp.has_output_material
        assert mpp.has_output_material_module
        assert mpp.is_data_only
        assert mpp.is_handmade
        assert mpp.output_material == [1, 2, 3, 4, 5]
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_data_only_package_03():
    '''Make data package. Delete material definition module.
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input=
            'm d testdata default default '
            'testdata mdd default q')
        assert studio.package_exists('baca.materials.testdata')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py']
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_data_only_package_04():
    '''Make data package. Overwrite material definition module with stub.
    Delete package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input=
            'm d testdata default default '
            'testdata mdt default q')
        assert studio.package_exists('baca.materials.testdata')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_data_only_package_05():
    '''Make data package. Copy canned material definition. Make data. Remove output material.
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input=
            'm d testdata default default '
            'testdata mdcanned canned_testdata_material_definition.py default '
            'dc default '
            'dd default q')
        assert studio.package_exists('baca.materials.testdata')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert not mpp.initializer_file_proxy.has_safe_import('output_material', 'testdata')
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_data_only_package_06():
    '''Make data package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    try:
        studio.run(user_input=
            'm d testdata default default '
            'testdata mdcanned canned_testdata_material_definition_with_exception.py default q')
        assert studio.package_exists('baca.materials.testdata')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
        assert mpp.has_faulty_material_definition
    finally:
        studio.run(user_input='m testdata del remove default q')
        assert not studio.package_exists('baca.materials.testdata')
