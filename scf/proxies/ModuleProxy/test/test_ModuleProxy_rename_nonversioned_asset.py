import os
import py
import scf
py.test.skip('make this work.')


def test_ModuleProxy_rename_nonversioned_asset_01():

    module_importable_name = 'scf.__temporary_module'
    module_proxy = scf.proxies.ModuleProxy(module_importable_name=module_importable_name)
    path_name = module_proxy.path_name
    assert not os.path.exists(path_name)

    try:
        module_proxy.conditionally_make_empty_asset() 
        assert os.path.exists(path_name)
        assert not module_proxy.is_versioned
        new_path_name = os.path.join(module_proxy.parent_directory_name, '__new_temporary_module')
        module_proxy.rename_nonversioned_asset(new_path_name)
        assert module_proxy.path_name == new_path_name
        module_proxy.remove()
    finally:
        #os.remove(path_name)
        #os.remove(new_path_name)
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)
