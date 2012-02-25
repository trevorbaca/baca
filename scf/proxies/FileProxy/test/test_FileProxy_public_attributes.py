import os
import scf


def test_FileProxy_public_attributes_01():
    '''Without path.
    '''

    file_proxy = scf.proxies.FileProxy()

    assert not file_proxy.file_lines
    assert file_proxy.generic_class_name == 'file'
    assert file_proxy.human_readable_name is None
    assert not file_proxy.is_in_repository
    assert file_proxy.parent_directory_name is None
    assert file_proxy.path_name is None
    assert file_proxy.plural_generic_class_name == 'files'
    assert file_proxy.short_name is None
    assert file_proxy.short_name_without_extension is None
    assert file_proxy.svn_add_command is None
        

def test_FileProxy_public_attributes_02():
    '''With path.
    '''

    path_name = os.path.join(os.environ.get('SCF'), 'stylesheets', 'clean_letter_14.ly')
    file_proxy = scf.proxies.FileProxy(path_name)
    
    assert file_proxy.file_lines
