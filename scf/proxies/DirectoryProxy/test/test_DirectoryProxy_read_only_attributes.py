import baca


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    directory_proxy = baca.scf.proxies.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scm')
    assert directory_proxy.path_name == '/Users/trevorbaca/Documents/other/baca/scm'
    assert directory_proxy.is_in_repository


def test_DirectoryProxy_read_only_attributes_02():
    
    directory_proxy_1 = baca.scf.proxies.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scf')
    directory_proxy_2 = baca.scf.proxies.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scf')
    directory_proxy_3 = baca.scf.proxies.DirectoryProxy('/Users/trevorbaca/Documents/other/baca')

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
