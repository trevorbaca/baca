import baca


def test_DirectoryProxy_01():
    '''Unnamed directory proxy.
    '''

    directory_proxy = baca.scf.DirectoryProxy()
    assert directory_proxy.directory_name is None
    assert not directory_proxy.has_directory 
    assert not directory_proxy.is_in_repository



def test_DirectoryProxy_02():
    '''Named directory proxy not yet written to disk.
    '''

    directory_proxy = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/foo')
    assert directory_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/foo'
    assert not directory_proxy.has_directory 
    assert not directory_proxy.is_in_repository


def test_DirectoryProxy_03():
    '''Named directory proxy already written to disk.
    '''

    directory_proxy = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scm')
    assert directory_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/scm'
    assert directory_proxy.has_directory 
    assert directory_proxy.is_in_repository


def test_DirectoryProxy_04():
    
    directory_proxy_1 = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scf')
    directory_proxy_2 = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scf')
    directory_proxy_3 = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca')

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
