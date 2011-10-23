import baca


def test_PackageProxy_01():
    '''Unnamed package proxy.
    '''

    package_proxy = baca.scf.PackageProxy()
    assert package_proxy.creation_date is None
    assert package_proxy.directory_name is None
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.get_tags() == {}
    assert not package_proxy.has_directory
    assert package_proxy.initializer_file_name is None
    assert not package_proxy.is_in_repository
    assert package_proxy.list_formatted_tags() == []
    assert package_proxy.package_importable_name is None
    assert package_proxy.package_short_name is None
    assert package_proxy.package_spaced_name is None 
    assert package_proxy.parent_initializer_file_name is None
    assert package_proxy.parent_package_importable_name is None
    assert package_proxy.purview is None
    assert package_proxy.score is None


def test_PackageProxy_02():
    '''Named package proxy not yet written to disk.
    '''

    package_proxy = baca.scf.PackageProxy('baca.foo')
    assert package_proxy.creation_date is None
    assert package_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/foo'
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.get_tags() == {}
    assert not package_proxy.has_directory
    assert package_proxy.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/foo/__init__.py'
    assert not package_proxy.is_in_repository
    assert package_proxy.list_formatted_tags() == []
    assert package_proxy.package_importable_name == 'baca.foo'
    assert package_proxy.package_short_name == 'foo'
    assert package_proxy.package_spaced_name == 'foo'
    assert package_proxy.parent_initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    assert package_proxy.parent_package_importable_name == 'baca'
    assert package_proxy.purview.is_studio_global_purview
    assert package_proxy.score is None


def test_PackageProxy_03():
    '''Package proxy (not yet written to disk) with only purview assigned.
    '''

    package_proxy = baca.scf.PackageProxy()
    package_proxy.purview = baca.scf.StudioInterface()

    assert package_proxy.directory_name is None
    assert package_proxy.package_importable_name is None
    assert package_proxy.package_short_name is None
    assert package_proxy.package_spaced_name is None 
    assert isinstance(package_proxy.purview, baca.scf.StudioInterface)
    assert package_proxy.score is None


def test_PackageProxy_04():
    '''Package proxy (not yet written to disk) with only package short name assigned.
    '''

    package_proxy = baca.scf.PackageProxy()
    package_proxy.package_short_name = 'foo'

    assert package_proxy.directory_name is None
    assert package_proxy.package_importable_name is None
    assert package_proxy.package_short_name == 'foo'
    assert package_proxy.package_spaced_name == 'foo'
    assert package_proxy.purview is None
    assert package_proxy.score is None
