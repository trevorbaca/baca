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
    '''Make data package. Create output material. Delete package." 
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default '
        'testdata mdcanned canned_testdata_material_definition.py default '
        'dc default q')
    assert studio.package_exists('baca.materials.testdata')

    mpp = baca.scf.MaterialPackageProxy('baca.materials.testdata')
    assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']

    assert     mpp.breadcrumb == 'testdata'
    assert not mpp.has_illustration_builder_module
    assert not mpp.has_illustration_ly
    assert not mpp.has_illustration_pdf
    assert     mpp.has_material_definition
    assert     mpp.has_material_definition_module
    assert not mpp.has_material_package_maker
    assert     mpp.has_output_material
    assert     mpp.has_output_material_module
    assert not mpp.has_user_input_module
    assert not mpp.has_user_input_wrapper
    assert     mpp.illustration is None
    assert     mpp.illustration_builder_module_file_name is None
    assert     mpp.illustration_builder_module_importable_name is None
    assert     mpp.illustration_builder_module_proxy is None
    assert     mpp.illustration_ly_file_name is None
    assert     mpp.illustration_ly_file_proxy is None
    assert     mpp.illustration_pdf_file_name is None
    assert     mpp.illustration_pdf_file_proxy is None
    assert     mpp.is_data_only
    assert     mpp.is_handmade
    assert     mpp.material_definition_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/testdata/material_definition.py'
    assert     mpp.material_definition_module_importable_name == \
        'baca.materials.testdata.material_definition'
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        '/Users/trevorbaca/Documents/other/baca/materials/testdata'
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_short_name == 'testdata'
    assert     mpp.material_spaced_name == 'testdata'
    assert     mpp.material_underscored_name == 'testdata'
    assert     mpp.materials_directory_name == \
        '/Users/trevorbaca/Documents/other/baca/materials'
    assert     mpp.materials_package_importable_name == 'baca.materials'
    assert     mpp.output_material == [1, 2, 3, 4, 5]
    assert     mpp.output_material_module_body_lines == ['testdata = [1, 2, 3, 4, 5]']
    assert     mpp.output_material_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/testdata/output_material.py'
    assert     mpp.output_material_module_importable_name == \
        'baca.materials.testdata.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert not  mpp.should_have_illustration
    assert not  mpp.should_have_illustration_builder_module
    assert not  mpp.should_have_illustration_ly
    assert not  mpp.should_have_illustration_pdf
    assert      mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert not  mpp.should_have_user_input_module
    assert      mpp.stylesheet_file_name is None
    assert      mpp.stylesheet_file_proxy is None
    assert      mpp.user_input_module_file_name is None
    assert      mpp.user_input_module_importable_name is None
    assert      mpp.user_input_module_proxy is None

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')
