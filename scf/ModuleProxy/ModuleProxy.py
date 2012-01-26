from baca.scf.ParsableFileProxy import ParsableFileProxy
import os


class ModuleProxy(ParsableFileProxy):

    def __init__(self, module_importable_name, session=None):
        assert isinstance(module_importable_name, str), '{!r} is not a string.'.format(module_importable_name)
        full_file_name = self.module_importable_name_to_full_file_name(module_importable_name)
        ParsableFileProxy.__init__(self, full_file_name, session=session)
        self._module_importable_name = module_importable_name

    ### READ-ONLY ATTRIBUTES ###

    # TODO: abstract out to MaterialModuleProxy
    @property
    def material_package_importable_name(self):
        return self.parent_module_importable_name
    
    # TODO: abstract out to MaterialModuleProxy
    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    # TODO: abstract out to MaterialModuleProxy
    @property
    def material_underscored_name(self):
        return self.module_importable_name.split('.')[-2]

    # TODO: abstract out to MaterialModuleProxy
    @property
    def materials_package_importable_name(self):
        return '.'.join(self.parent_module_importable_name.split('.')[:-1])
    
    @property
    def module_importable_name(self):
        return self._module_importable_name

    @property
    def module_short_name(self):
        return self.module_importable_name.split('.')[-1]

    @property
    def parent_module_importable_name(self):
        return '.'.join(self.module_importable_name.split('.')[:-1])

    ### PUBLIC METHODS ###

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.full_file_name))
        self.display('file executed', prompt=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.full_file_name))
        self.proceed('file executed.', prompt=prompt)

    def unimport(self):
        self.remove_package_importable_name_from_sys_modules(self.module_importable_name)

    # TODO: abstract out to MaterialModuleProxy
    def unimport_material_package(self):
        self.remove_package_importable_name_from_sys_modules(self.material_package_importable_name)

    # TODO: abstract out to MaterialModuleProxy
    def unimport_materials_package(self):
        self.remove_package_importable_name_from_sys_modules(self.materials_package_importable_name)
