import baca
import types


def test_GlobalProxy_01():
    '''Attributes.
    '''

    global_proxy = baca.scf.GlobalProxy()
    assert global_proxy.class_name == 'GlobalProxy'
    assert global_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert global_proxy.get_tag('foo') is None
    assert global_proxy.get_tags() == {}
    assert global_proxy.has_directory
    assert global_proxy.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    assert not global_proxy.is_score_local_purview
    assert global_proxy.is_studio_global_purview
    assert global_proxy.list_formatted_tags() == []
    assert global_proxy.maker_wrangler == baca.scf.MakerWrangler()
    assert global_proxy.material_wrangler == baca.scf.MaterialWrangler('baca')
    assert global_proxy.materials_package_importable_name == 'baca.materials'
    assert global_proxy.package_importable_name == 'baca'
    assert global_proxy.package_short_name == 'baca'
    assert global_proxy.package_spaced_name == 'baca'
    assert global_proxy.parent_initializer_file_name is None
    assert global_proxy.parent_package_importable_name is None
    assert global_proxy.purview == global_proxy
    assert global_proxy.score is None
    assert global_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/GlobalProxy/GlobalProxy.py'
    assert global_proxy.spaced_class_name == 'global proxy'


def test_GlobalProxy_02():
    '''Straightforward methods.
    '''

    global_proxy = baca.scf.GlobalProxy()
    
    assert isinstance(global_proxy.import_attribute_from_initializer('scf'), types.ModuleType)


def test_GlobalProxy_03():
    '''Shared session.
    '''

    global_proxy = baca.scf.GlobalProxy()

    assert global_proxy.session is global_proxy.maker_wrangler.session
    assert global_proxy.session is global_proxy.material_wrangler.session
