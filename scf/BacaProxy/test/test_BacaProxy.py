import baca


def test_BacaProxy_01():

    baca_proxy = baca.scf.BacaProxy()
    assert baca_proxy.creation_date is None
    assert baca_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert baca_proxy.get_tag('foo') is None
    assert baca_proxy.get_tags() == {}
    assert baca_proxy.has_directory
    assert baca_proxy.initializer_file_name == '/Users/trevorbaca/Documents/other/baca/__init__.py'
    # TODO: find robust way to check repository check-in status
    #assert baca_proxy.is_in_repository
    assert not baca_proxy.is_score_local_purview
    assert baca_proxy.is_studio_global_purview
    assert baca_proxy.list_formatted_tags() == []
    assert baca_proxy.package_importable_name == 'baca'
    assert baca_proxy.package_short_name == 'baca'
    assert baca_proxy.package_spaced_name == 'baca'
    assert baca_proxy.parent_initializer_file_name is None
    assert baca_proxy.parent_package_importable_name is None
    assert baca_proxy.score is None
