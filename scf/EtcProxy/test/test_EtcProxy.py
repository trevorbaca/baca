import baca


def test_EtcProxy_01():

    etc_proxy = baca.scf.EtcProxy('manos')

    assert etc_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/etc'
    assert etc_proxy.has_directory
    assert etc_proxy.is_in_repository
    assert etc_proxy.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/EtcProxy/EtcProxy.py'
    assert etc_proxy.spaced_class_name == 'etc proxy'
