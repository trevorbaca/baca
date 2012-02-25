import scf


def test_PackageProxy_read_only_attributes_01():
    '''Stub package.
    '''

    package_proxy = scf.proxies.PackageProxy('baca.materials.red_sargasso')
    assert package_proxy.path_name == '/Users/trevorbaca/Documents/other/baca/materials/red_sargasso'
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/red_sargasso/__init__.py'
    assert package_proxy.importable_name == 'baca.materials.red_sargasso'
    assert package_proxy.short_name == 'red_sargasso'
    assert package_proxy.human_readable_name == 'red sargasso'
    assert package_proxy.parent_initializer_file_name == \
        '/Users/trevorbaca/Documents/other/baca/materials/__init__.py'
    assert package_proxy.parent_package_importable_name == 'baca.materials'
    assert package_proxy.score is None
