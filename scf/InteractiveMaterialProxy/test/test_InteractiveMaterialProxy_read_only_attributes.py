import baca


def test_InteractiveMaterialProxy_read_only_attributes_01():

    imp = baca.scf.InteractiveMaterialProxy('baca.materials.test_measures_a')
    assert imp.has_input_data
    assert imp.has_input_file
    assert imp.has_output_data
    assert imp.has_output_file
    assert not imp.has_score_definition
    assert imp.has_stylesheet
    assert imp.has_visualization_ly
    assert imp.has_visualization_pdf
    assert not imp.has_visualizer
    assert imp.input_file_name == '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/input.py'
    assert imp.input_package_importable_name == 'baca.materials.test_measures_a.input'
    assert not imp.is_in_score
    assert imp.is_interactive
    assert imp.is_shared
    assert not imp.is_static
    assert imp.material_spaced_name == 'test measures a'
    assert imp.material_underscored_name == 'test_measures_a'
    assert imp.materials_package_importable_name == 'baca.materials'
    assert imp.output_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/output.py'
    assert imp.output_package_importable_name == 'baca.materials.test_measures_a.output'
    assert imp.score_package_short_name == 'baca'
    assert imp.stylesheet_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/stylesheet.ly'
    assert isinstance(imp.user_input_wrapper, baca.scf.UserInputWrapper)
    assert imp.visualizer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/visualization.py'
    assert imp.visualization_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/visualization.ly'
    assert imp.visualization_package_importable_name == 'baca.materials.test_measures_a.visualization'
    assert imp.visualization_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/visualization.pdf'
