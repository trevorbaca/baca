import baca


def test_StaticMaterialProxy_read_only_attributes_01():
    '''Attributes.
    '''

    smp = baca.scf.StaticMaterialProxy('baca.materials.sargasso_multipliers')
    assert smp.has_input_data
    assert smp.has_material_definition
    assert smp.has_output_data
    assert smp.has_output_file
    assert not smp.has_score_definition
    assert not smp.has_stylesheet
    assert not smp.has_visualization_ly
    assert not smp.has_visualization_pdf
    assert not smp.has_score_builder
    assert smp.material_definition_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/input.py'
    assert smp.input_package_importable_name == 'baca.materials.sargasso_multipliers.input'
    assert not smp.is_in_score
    assert not smp.is_interactive
    assert smp.is_shared
    assert smp.is_static
    assert smp.material_spaced_name == 'sargasso multipliers'
    assert smp.material_underscored_name == 'sargasso_multipliers'
    assert smp.materials_package_importable_name == 'baca.materials'
    assert smp.output_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/output.py'
    assert smp.output_package_importable_name == 'baca.materials.sargasso_multipliers.output'
    assert smp.score_package_short_name == 'baca'
    assert smp.stylesheet_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/stylesheet.ly'
    assert smp.score_builder_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/visualization.py'
    assert smp.visualization_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/visualization.ly'
    assert smp.visualization_package_importable_name == 'baca.materials.sargasso_multipliers.visualization'
    assert smp.visualization_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/visualization.pdf'
