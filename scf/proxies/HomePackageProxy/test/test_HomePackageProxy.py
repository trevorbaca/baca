import scf
import types


def test_HomePackageProxy_01():
    '''Attributes.
    '''

    hpp = scf.proxies.HomePackageProxy()
    assert hpp.class_name == 'HomePackageProxy'
    assert hpp.path_name == '/Users/trevorbaca/Documents/other/baca'
    assert hpp.get_tag('foo') is None
    assert hpp.get_tags() == {}
    assert hpp.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    assert hpp.formatted_tags == []
    assert hpp.importable_name == 'baca'
    assert hpp.short_name == 'baca'
    assert hpp.human_readable_name == 'baca'
    assert hpp.parent_initializer_file_name is None
    assert hpp.parent_package_importable_name is None
    assert hpp.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/proxies/HomePackageProxy/HomePackageProxy.py'
    assert hpp.spaced_class_name == 'home package proxy'
