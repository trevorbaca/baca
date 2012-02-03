import baca
import py


def test_MaterialPackageWrangler_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.ts == (4,)

    studio.run(user_input='m b q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='m studio q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='m score q')
    assert studio.ts == (6, (2, 4))

    studio.run(user_input='m asdf q')
    assert studio.ts == (6, (2, 4))


def test_MaterialPackageWrangler_run_02():
    '''Breadcrumbs work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.transcript[-2][0] == 'Studio - materials'


def test_MaterialPackageWrangler_run_03():
    '''Make data package. Delete package.
    '''
    
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default q')
    assert studio.package_exists('baca.materials.testdata')

    mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
    assert mpp.directory_contents == ['__init__.py', 'material_definition.py']

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_04():
    '''Make data package. Create output material. Test. Delete package." 
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default '
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

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_05():
    '''Make data package.
    Delete material definition module. Test. 
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default '
        'testdata mdd default q')
    assert studio.package_exists('baca.materials.testdata')

    mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
    assert mpp.directory_contents == ['__init__.py']

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_06():
    '''Make data package. Overwrite material definition module with stub. Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default '
        'testdata mdt default q')
    assert studio.package_exists('baca.materials.testdata')

    mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
    assert mpp.directory_contents == ['__init__.py', 'material_definition.py']

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_07():
    '''Make data package. Copy canned material definition. Make data. Remove output material.
    Remove package.
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input=
        'm d testdata default default '
        'testdata mdcanned canned_testdata_material_definition.py default '
        'dc default '
        'dd default q')
    assert studio.package_exists('baca.materials.testdata')

    mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
    assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
    # TODO: make this work
    #assert not mpp.initializer_file_proxy.has_safe_import('output_material', 'testdata')

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')
