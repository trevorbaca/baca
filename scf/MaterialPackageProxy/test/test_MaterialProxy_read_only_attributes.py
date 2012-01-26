import baca


def test_MaterialPackageProxy_read_only_attributes_01():
    '''Stub material.
    '''

    material_proxy = baca.scf.MaterialPackageProxy('baca.materials.test_measures_a')
    assert not material_proxy.has_material_definition
    assert not material_proxy.has_material_definition_module
    assert material_proxy.has_output_material
    assert material_proxy.has_output_material_module
    assert material_proxy.has_illustration_ly
    assert material_proxy.has_illustration_pdf
    assert not material_proxy.has_illustration_builder
    assert material_proxy.material_definition_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/material_definition.py'
    assert material_proxy.material_definition_module_importable_name == \
        'baca.materials.test_measures_a.material_definition'
    assert material_proxy.has_material_package_maker
    assert material_proxy.material_spaced_name == 'test measures a'
    assert material_proxy.material_underscored_name == 'test_measures_a'
    assert material_proxy.output_material_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/output_material.py'
    assert material_proxy.output_material_module_importable_name == \
        'baca.materials.test_measures_a.output_material'
    assert material_proxy.score_package_short_name == 'baca'
    assert material_proxy.illustration_builder_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/illustration_builder.py'
    assert material_proxy.illustration_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_measures_a/illustration.ly'
    assert material_proxy.illustration_builder_module_importable_name == \
        'baca.materials.test_measures_a.illustration_builder'
    assert material_proxy.illustration_pdf_file_name == \
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
    assert not smp.has_illustration_builder
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
    assert smp.score_package_short_name == 'baca'
    assert smp.illustration_builder_module_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration_builder.py'
    assert smp.illustration_ly_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration.ly'
    assert smp.illustration_builder_module_importable_name == 'baca.materials.sargasso_multipliers.illustration_builder'
    assert smp.illustration_pdf_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/sargasso_multipliers/illustration.pdf'
