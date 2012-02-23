import baca


def test_EtcDirectoryProxy_01():

    etc_proxy = baca.scf.proxies.EtcDirectoryProxy('manos')

    assert etc_proxy.path_name == '/Users/trevorbaca/Documents/scores/manos/etc'
    assert etc_proxy.is_in_repository
    assert etc_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/proxies/EtcDirectoryProxy/EtcDirectoryProxy.py'
    assert etc_proxy.spaced_class_name == 'etc directory proxy'
