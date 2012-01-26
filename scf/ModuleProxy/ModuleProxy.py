from baca.scf.ParsableFileProxy import ParsableFileProxy


class ModuleProxy(ParsableFileProxy):

    def __init__(self, module_importable_name, session=None):
        assert isinstance(module_importable_name, str), '{!r} is not a string.'.format(module_importable_name)
        full_file_name = self.module_importable_name_to_full_file_name(module_importable_name)
        ParsableFileProxy.__init__(self, full_file_name, session=session)
        self._module_importable_name = module_importable_name

    ### READ-ONLY ATTRIBUTES ###

    # TODO: abstract out to MaterialModuleProxy
    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    # TODO: abstract out to MaterialModuleProxy
    @property
    def material_underscored_name(self):
        return self.module_importable_name.split('.')[-2]

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

    def unimport(self):
        self.remove_package_importable_name_from_sys_modules(self.module_importable_name)
