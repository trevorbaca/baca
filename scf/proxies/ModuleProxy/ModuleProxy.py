from scf.proxies.ImportableAssetProxy import ImportableAssetProxy
from scf.proxies.ParsableFileProxy import ParsableFileProxy
import os


class ModuleProxy(ParsableFileProxy, ImportableAssetProxy):

    def __init__(self, module_importable_name=None, session=None):
        module_importable_name = self.strip_py_extension(module_importable_name)
        path_name = self.module_importable_name_to_path_name(module_importable_name)
        ParsableFileProxy.__init__(self, path_name=path_name, session=session)
        ImportableAssetProxy.__init__(self, asset_full_name=path_name, session=self.session)

    ### OVERLOADS ###

    def __repr__(self):
        return ImportableAssetProxy.__repr__(self)

    ### READ-ONLY ATTRIBUTES ###

    @property
    def grandparent_package_directory_name(self):
        return self.package_importable_name_to_path_name(self.grandparent_package_importable_name)

    @property
    def grandparent_package_importable_name(self):
        return self.dot_join(self.module_importable_name.split('.')[:-2])

    @property
    def grandparent_package_initializer_file_name(self):
        return os.path.join(self.grandparent_package_directory_name, '__init__.py')

    @property
    def human_readable_name(self):
        return self.short_name_without_extension

    @property
    def module_importable_name(self):
        return self.importable_name

    @property
    def module_short_name(self):
        return self.module_importable_name.split('.')[-1]

    @property
    def parent_package_directory_name(self):
        return self.package_importable_name_to_path_name(self.parent_package_importable_name)

    @property
    def parent_package_importable_name(self):
        return self.dot_join(self.module_importable_name.split('.')[:-1])

    @property
    def parent_package_initializer_file_name(self):
        return os.path.join(self.parent_package_directory_name, '__init__.py')

    @property
    def temporary_asset_short_name(self):
        return '__temporary_module.py'
        
    ### PUBLIC METHODS ###

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.path_name))
        self.proceed('file executed', prompt=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.path_name))
        self.proceed('file executed.', prompt=prompt)

    def unimport(self):
        self.remove_package_importable_name_from_sys_modules(self.module_importable_name)
