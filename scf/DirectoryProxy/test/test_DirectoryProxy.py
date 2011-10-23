import baca


def test_DirectoryProxy_01():
    '''Unnamed directory proxy.
    '''

    directory_proxy = baca.scf.DirectoryProxy()
    assert directory_proxy.directory_name is None
    assert not directory_proxy.has_directory 
    assert not directory_proxy.is_in_repository
    assert directory_proxy.parent_directory_name is None



def test_DirectoryProxy_02():
    '''Named directory proxy not yet written to disk.
    '''

    directory_proxy = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/foo')
    assert directory_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/foo'
    assert not directory_proxy.has_directory 
    assert not directory_proxy.is_in_repository
    assert directory_proxy.parent_directory_name == '/Users/trevorbaca/Documents/other/baca'


def test_DirectoryProxy_03():
    '''Named directory proxy already written to disk.
    '''

    directory_proxy = baca.scf.DirectoryProxy('/Users/trevorbaca/Documents/other/baca/scm')
    assert directory_proxy.directory_name == '/Users/trevorbaca/Documents/other/baca/scm'
    assert directory_proxy.has_directory 
    assert directory_proxy.is_in_repository
    assert directory_proxy.parent_directory_name == '/Users/trevorbaca/Documents/other/baca'
