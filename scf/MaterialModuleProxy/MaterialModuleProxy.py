from baca.scf.ModuleProxy import ModuleProxy


class MaterialModuleProxy(ModuleProxy):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def material_package_importable_name(self):
        return self.parent_module_importable_name

    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    @property
    def material_underscored_name(self):
        return self.module_importable_name.split('.')[-2]

    @property
    def materials_package_importable_name(self):
        return '.'.join(self.parent_module_importable_name.split('.')[:-1])
