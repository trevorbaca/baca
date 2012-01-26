import baca
import py


def test_MaterialPackageProxy_read_only_attributes_01():
    '''Data-only package.
    '''
    
    mpp = baca.scf.MaterialPackageProxy('baca.materials.red_numbers')
    assert     mpp.breadcrumb == 'red numbers'
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
    assert     mpp.illustration_builder_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/illustration_builder.py'
    assert     mpp.illustration_builder_module_importable_name == \
        'baca.materials.red_numbers.illustration_builder'
    assert     mpp.illustration_builder_module_proxy is None
    assert     mpp.illustration_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/illustration.ly'
    assert     mpp.illustration_ly_file_proxy is None
    assert     mpp.illustration_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/illustration.pdf'
    assert     mpp.illustration_pdf_file_proxy is None
    assert not mpp.is_changed   
    assert     mpp.is_data_only
    assert     mpp.is_handmade
    assert     mpp.material_definition_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/material_definition.py'
    assert     mpp.material_definition_module_importable_name == \
        'baca.materials.red_numbers.material_definition' 
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers'
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_short_name == 'red_numbers'
    assert     mpp.material_spaced_name == 'red numbers'
    assert     mpp.material_underscored_name == 'red_numbers'
    assert     mpp.materials_directory_name == \
        '/Users/trevorbaca/Documents/other/baca/materials'
    assert     mpp.materials_package_importable_name == 'baca.materials'
    assert     mpp.output_material == [1, 2, 3, 4, 5]
    assert     mpp.output_material_module_body_lines == ['red_numbers = [1, 2, 3, 4, 5]']
    assert     mpp.output_material_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/output_material.py'
    assert     mpp.output_material_module_importable_name == \
        'baca.materials.red_numbers.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert not  mpp.should_have_illustration
    assert      mpp.source_stylesheet_file_name is None
    assert      mpp.source_stylesheet_file_proxy is None
    assert      mpp.user_input_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_numbers/user_input.py'
    assert      mpp.user_input_module_importable_name == \
        'baca.materials.red_numbers.user_input'
    assert      mpp.user_input_module_proxy is None


def test_MaterialPackageProxy_read_only_attributes_02():
    '''Maker material.
    '''

    mpp = baca.scf.MaterialPackageProxy('baca.materials.test_measures_a')
    assert not mpp.has_material_definition
    assert not mpp.has_material_definition_module
    assert mpp.has_output_material
    assert mpp.has_output_material_module
    assert mpp.has_illustration_ly
    assert mpp.has_illustration_pdf
    assert not mpp.has_illustration_builder
    assert mpp.material_definition_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/material_definition.py'
    assert mpp.material_definition_module_importable_name == \
        'baca.materials.test_measures_a.material_definition'
    assert mpp.has_material_package_maker
    assert mpp.material_spaced_name == 'test measures a'
    assert mpp.material_underscored_name == 'test_measures_a'
    assert mpp.output_material_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/output_material.py'
    assert mpp.output_material_module_importable_name == \
        'baca.materials.test_measures_a.output_material'
    assert mpp.score_package_short_name == 'baca'
    assert mpp.illustration_builder_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/illustration_builder.py'
    assert mpp.illustration_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/illustration.ly'
    assert mpp.illustration_builder_module_importable_name == \
        'baca.materials.test_measures_a.illustration_builder'
    assert mpp.illustration_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/illustration.pdf'


def test_MaterialPackageProxy_read_only_attributes_02():
    '''Data-only material (without illustration).
    '''

    smp = baca.scf.MaterialPackageProxy('baca.materials.sargasso_multipliers')
    assert smp.has_material_definition
    assert smp.has_material_definition_module
    assert smp.has_output_material
    assert smp.has_output_material_module
    assert not smp.has_illustration_ly
    assert not smp.has_illustration_pdf
    assert not smp.has_illustration_builder_module
    assert smp.material_definition_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/material_definition.py'
    assert smp.material_definition_module_importable_name == \
        'baca.materials.sargasso_multipliers.material_definition'
    assert not smp.has_material_package_maker
    assert smp.material_spaced_name == 'sargasso multipliers'
    assert smp.material_underscored_name == 'sargasso_multipliers'
    assert smp.output_material_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/output_material.py'
    assert smp.output_material_module_importable_name == 'baca.materials.sargasso_multipliers.output_material'
    assert smp.illustration_builder_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration_builder.py'
    assert smp.illustration_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration.ly'
    assert smp.illustration_builder_module_importable_name == 'baca.materials.sargasso_multipliers.illustration_builder'
    assert smp.illustration_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration.pdf'
