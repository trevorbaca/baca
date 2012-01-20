import baca


def test_EtcDirectoryProxy_01():

    etc_proxy = baca.scf.EtcDirectoryProxy('manos')

    assert etc_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/etc'
    assert etc_proxy.is_in_repository
    assert etc_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/EtcDirectoryProxy/EtcDirectoryProxy.py'
    assert etc_proxy.spaced_class_name == 'etc directory proxy'
