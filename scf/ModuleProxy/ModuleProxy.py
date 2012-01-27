from baca.scf.ParsableFileProxy import ParsableFileProxy
import os


class ModuleProxy(ParsableFileProxy):

    def __init__(self, module_importable_name, session=None):
        assert isinstance(module_importable_name, str), '{!r} is not a string.'.format(module_importable_name)
        full_file_name = self.module_importable_name_to_full_file_name(module_importable_name)
        ParsableFileProxy.__init__(self, full_file_name, session=session)
        self._module_importable_name = module_importable_name

    ### READ-ONLY ATTRIBUTES ###

    @property
    def grandparent_package_directory_name(self):
        return self.package_importable_name_to_directory_name(self.grandparent_package_importable_name)

    @property
    def grandparent_package_importable_name(self):
        return '.'.join(self.module_importable_name.split('.')[:-2])

    @property
    def grandparent_package_initializer_file_name(self):
        return os.path.join(self.grandparent_package_directory_name, '__init__.py')

    @property
    def module_importable_name(self):
        return self._module_importable_name

    @property
    def module_short_name(self):
        return self.module_importable_name.split('.')[-1]

    @property
    def parent_package_directory_name(self):
        return self.package_importable_name_to_directory_name(self.parent_package_importable_name)

    @property
    def parent_package_importable_name(self):
        return '.'.join(self.module_importable_name.split('.')[:-1])

    @property
    def parent_package_initializer_file_name(self):
        return os.path.join(self.parent_package_directory_name, '__init__.py')
        
    ### PUBLIC METHODS ###

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.full_file_name))
        self.display('file executed', prompt=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.full_file_name))
        self.proceed('file executed.', prompt=prompt)

    def unimport(self):
        self.remove_package_importable_name_from_sys_modules(self.module_importable_name)
