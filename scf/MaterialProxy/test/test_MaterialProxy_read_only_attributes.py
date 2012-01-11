import baca


def test_MaterialProxy_read_only_attributes_01():
    '''Stub material.
    '''

    material_proxy = baca.scf.MaterialProxy('baca.materials.test_material_a')
    assert not material_proxy.has_material_definition
    assert not material_proxy.has_material_definition_module
    assert not material_proxy.has_output_data
    assert not material_proxy.has_output_data_module
    assert not material_proxy.has_score_definition
    assert not material_proxy.has_stylesheet
    assert not material_proxy.has_visualization_ly
    assert not material_proxy.has_visualization_pdf
    assert not material_proxy.has_score_builder
    assert material_proxy.material_definition_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/input.py'
    assert material_proxy.material_definition_module_importable_name == 'baca.materials.test_material_a.input'
    assert not material_proxy.is_in_score
    assert not material_proxy.is_interactive
    assert material_proxy.is_shared
    assert material_proxy.is_static
    assert material_proxy.material_spaced_name == 'test material a'
    assert material_proxy.material_underscored_name == 'test_material_a'
    assert material_proxy.materials_package_importable_name == 'baca.materials'
    assert material_proxy.output_data_module_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/output.py'
    assert material_proxy.output_data_module_importable_name == 'baca.materials.test_material_a.output'
    assert material_proxy.score_package_short_name == 'baca'
    assert material_proxy.stylesheet_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/stylesheet.ly'
    assert material_proxy.user_input_wrapper is None
    assert material_proxy.score_builder_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/visualization.py'
    assert material_proxy.visualization_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/visualization.ly'
    assert material_proxy.visualization_package_importable_name == \
        'baca.materials.test_material_a.visualization'
    assert material_proxy.visualization_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/visualization.pdf'
