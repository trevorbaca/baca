from baca.scf.ParsableFileProxy import ParsableFileProxy


class ModuleProxy(ParsableFileProxy):

    def __init__(self, module_importable_name, session=None):
        assert isinstance(module_importable_name, str), '{!r} is not a string.'.format(module_importable_name)
        full_file_name = self.module_importable_name_to_full_file_name(module_importable_name)
        ParsableFileProxy.__init__(self, full_file_name, session=session)
        self._module_importable_name = module_importable_name

    ### READ-ONLY ATTRIBUTES ###

    @property
    def module_importable_name(self):
        return self._module_importable_name

    @property
    def module_short_name(self):
        return self.module_importable_name.split('.')[-1]
