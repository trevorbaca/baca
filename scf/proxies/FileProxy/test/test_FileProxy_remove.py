import os
import scf


def test_FileProxy_remove_01():
    '''Nonversioned file.
    '''

    path_name = os.path.join(os.environ.get('SCF'), 'temporary_file.txt')
    file_proxy = scf.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        file_proxy.remove()
        assert not os.path.exists(path_name)
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        assert not os.path.exists(path_name)


def test_FileProxy_remove_02():
    '''Versioned file.
    '''

    path_name = os.path.join(os.environ.get('SCF'), 'temporary_file.txt')
    file_proxy = scf.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        file_proxy.svn_add()
        assert file_proxy.is_versioned
        file_proxy.remove()
        assert not os.path.exists(path_name)
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        assert not os.path.exists(path_name)
