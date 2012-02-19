import baca
import types


def test_HomePackageProxy_01():
    '''Attributes.
    '''

    hpp = baca.scf.proxies.HomePackageProxy()
    assert hpp.class_name == 'HomePackageProxy'
    assert hpp.directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert hpp.get_tag('foo') is None
    assert hpp.get_tags() == {}
    assert hpp.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    assert hpp.formatted_tags == []
    assert hpp.material_package_maker_wrangler == baca.scf.wranglers.MaterialPackageMakerWrangler()
    assert hpp.material_package_wrangler == baca.scf.wranglers.MaterialPackageWrangler()
    assert hpp.current_materials_package_importable_name == 'baca.materials'
    assert hpp.package_importable_name == 'baca'
    assert hpp.package_short_name == 'baca'
    assert hpp.package_spaced_name == 'baca'
    assert hpp.parent_initializer_file_name is None
    assert hpp.parent_package_importable_name is None
    assert hpp.score is None
    assert hpp.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/proxies/HomePackageProxy/HomePackageProxy.py'
    assert hpp.spaced_class_name == 'home package proxy'


def test_HomePackageProxy_02():
    '''Shared session.
    '''

    hpp = baca.scf.proxies.HomePackageProxy()

    assert hpp.session is hpp.material_package_maker_wrangler.session
    assert hpp.session is hpp.material_package_wrangler.session
