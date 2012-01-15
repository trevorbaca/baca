import baca


def test_MaterialProxy_read_only_attributes_01():
    '''Stub material.
    '''

    material_proxy = baca.scf.materialproxies.MaterialProxy('baca.materials.test_material_a')
    assert not material_proxy.has_material_definition
    assert not material_proxy.has_material_definition_module
    assert not material_proxy.has_output_data
    assert not material_proxy.has_output_data_module
    assert not material_proxy.has_score_definition
    assert not material_proxy.has_local_stylesheet
    assert not material_proxy.has_output_ly
    assert not material_proxy.has_output_pdf
    assert not material_proxy.has_score_builder
    assert material_proxy.material_definition_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/material_definition.py'
    assert material_proxy.material_definition_module_importable_name == \
        'baca.materials.test_material_a.material_definition'
    assert not material_proxy.is_in_score
    assert not material_proxy.is_interactive
    assert material_proxy.is_shared
    assert material_proxy.is_static
    assert material_proxy.material_spaced_name == 'test material a'
    assert material_proxy.material_underscored_name == 'test_material_a'
    assert material_proxy.materials_package_importable_name == 'baca.materials'
    assert material_proxy.output_data_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/output.py'
    assert material_proxy.output_data_module_importable_name == 'baca.materials.test_material_a.output'
    assert material_proxy.score_package_short_name == 'baca'
    assert material_proxy.local_stylesheet_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/stylesheet.ly'
    assert material_proxy.user_input_wrapper is None
    assert material_proxy.score_builder_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/score_builder.py'
    assert material_proxy.output_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/output.ly'
    assert material_proxy.score_builder_module_importable_name == \
        'baca.materials.test_material_a.score_builder'
    assert material_proxy.output_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/output.pdf'


def test_MaterialProxy_read_only_attributes_02():
    '''Data-only material (without illustration).
    '''

    smp = baca.scf.materialproxies.MaterialProxy('baca.materials.sargasso_multipliers')
    assert smp.has_material_definition
    assert smp.has_material_definition_module
    assert smp.has_output_data
    assert smp.has_output_data_module
    assert not smp.has_score_definition
    assert not smp.has_local_stylesheet
    assert not smp.has_output_ly
    assert not smp.has_output_pdf
    assert not smp.has_score_builder
    assert smp.material_definition_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/material_definition.py'
    assert smp.material_definition_module_importable_name == \
        'baca.materials.sargasso_multipliers.material_definition'
    assert not smp.is_in_score
    assert not smp.is_interactive
    assert smp.is_shared
    assert smp.is_static
    assert smp.material_spaced_name == 'sargasso multipliers'
    assert smp.material_underscored_name == 'sargasso_multipliers'
    assert smp.materials_package_importable_name == 'baca.materials'
    assert smp.output_data_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/output.py'
    assert smp.output_data_module_importable_name == 'baca.materials.sargasso_multipliers.output'
    assert smp.score_package_short_name == 'baca'
    assert smp.local_stylesheet_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/stylesheet.ly'
    assert smp.score_builder_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/score_builder.py'
    assert smp.output_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/output.ly'
    assert smp.score_builder_module_importable_name == 'baca.materials.sargasso_multipliers.score_builder'
    assert smp.output_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/output.pdf'
