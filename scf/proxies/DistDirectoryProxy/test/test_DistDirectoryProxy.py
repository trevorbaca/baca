import baca


def test_DistDirectoryProxy_01():

    dist_proxy = baca.scf.proxies.DistDirectoryProxy('manos')

    assert dist_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/dist'
    assert dist_proxy.is_in_repository
    assert dist_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/proxies/DistDirectoryProxy/DistDirectoryProxy.py'
    assert dist_proxy.spaced_class_name == 'dist directory proxy'
