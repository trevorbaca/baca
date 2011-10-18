import baca


def test_MaterialProxy_01():
    '''Unnamed material.
    '''

    material_proxy = baca.scf.MaterialProxy.MaterialProxy()
    assert not material_proxy.has_input_data
    assert not material_proxy.has_input_file
    assert not material_proxy.has_output_data
    assert not material_proxy.has_output_file
    assert not material_proxy.has_score_definition
    assert not material_proxy.has_stylesheet
    assert not material_proxy.has_visualization_ly
    assert not material_proxy.has_visualization_pdf
    assert not material_proxy.has_visualizer
    assert material_proxy.input_file_name is None
    assert material_proxy.input_package_importable_name is None
    assert not material_proxy.is_in_score
    assert not material_proxy.is_interactive
    assert not material_proxy.is_shared
    assert material_proxy.is_static
    assert material_proxy.material_spaced_name is None
    assert material_proxy.material_underscored_name is None
    assert material_proxy.materials_package_importable_name is None
    assert material_proxy.output_file_name is None
    assert material_proxy.output_package_importable_name is None
    assert material_proxy.score_package_short_name is None
    assert material_proxy.stylesheet_file_name is None
    assert material_proxy.user_input_wrapper is None
    assert material_proxy.visualizer_file_name is None
    assert material_proxy.visualization_ly_file_name is None
    assert material_proxy.visualization_package_importable_name is None
    assert material_proxy.visualization_pdf_file_name is None
