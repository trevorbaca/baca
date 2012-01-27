import baca
import types


def test_HomePackageProxy_01():
    '''Attributes.
    '''

    global_proxy = baca.scf.HomePackageProxy()
    assert global_proxy.class_name == 'HomePackageProxy'
    assert global_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert global_proxy.get_tag('foo') is None
    assert global_proxy.get_tags() == {}
    assert global_proxy.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    assert global_proxy.formatted_tags == []
    assert global_proxy.material_proxy_wrangler == baca.scf.MaterialPackageMakerWrangler()
    assert global_proxy.material_wrangler == baca.scf.MaterialPackageWrangler()
    assert global_proxy.materials_package_importable_name == 'baca.materials'
    assert global_proxy.package_importable_name == 'baca'
    assert global_proxy.package_short_name == 'baca'
    assert global_proxy.package_spaced_name == 'baca'
    assert global_proxy.parent_initializer_file_name is None
    assert global_proxy.parent_package_importable_name is None
    assert global_proxy.score is None
    assert global_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/HomePackageProxy/HomePackageProxy.py'
    assert global_proxy.spaced_class_name == 'home package proxy'


def test_HomePackageProxy_02():
    '''Shared session.
    '''

    global_proxy = baca.scf.HomePackageProxy()

    assert global_proxy.session is global_proxy.material_proxy_wrangler.session
    assert global_proxy.session is global_proxy.material_wrangler.session
