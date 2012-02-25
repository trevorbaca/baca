import os
import scf


def test_FileProxy_public_attributes_01():
    '''Without path.
    '''

    file_proxy = scf.proxies.FileProxy()

    assert not file_proxy.file_lines
    #assert file_proxy.is_exceptionless
    #assert not file_proxy.sections


def test_FileProxy_public_attributes_02():
    '''With path.
    '''

    path_name = os.path.join(os.environ.get('SCF'), 'stylesheets', 'clean_letter_14.ly')
    file_proxy = scf.proxies.FileProxy(path_name)
    
    assert file_proxy.file_lines
    #assert file_proxy.is_exceptionless
    #assert not file_proxy.sections
