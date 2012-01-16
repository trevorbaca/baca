import baca


def test_PackageProxy_read_only_attributes_01():
    '''Stub package.
    '''

    package_proxy = baca.scf.PackageProxy('baca.materials.test_material_a')
    assert package_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/materials/test_material_a'
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.get_tags() == {}
    assert package_proxy.initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/test_material_a/__init__.py'
    #assert package_proxy.is_in_repository
    assert package_proxy.list_formatted_tags() == []
    assert package_proxy.package_importable_name == 'baca.materials.test_material_a'
    assert package_proxy.package_short_name == 'test_material_a'
    assert package_proxy.package_spaced_name == 'test material a'
    assert package_proxy.parent_initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/__init__.py'
    assert package_proxy.parent_package_importable_name == 'baca.materials'
    assert package_proxy.score is None
