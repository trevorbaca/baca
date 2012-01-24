import baca


def test_ExgDirectoryProxy_01():

    exg_proxy = baca.scf.ExgDirectoryProxy('manos')

    assert exg_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/exg'
    assert exg_proxy.is_in_repository
    assert exg_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/ExgDirectoryProxy/ExgDirectoryProxy.py'
    assert exg_proxy.spaced_class_name == 'exg directory proxy'
