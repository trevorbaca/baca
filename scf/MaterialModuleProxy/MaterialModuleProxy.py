from baca.scf.ModuleProxy import ModuleProxy


class MaterialModuleProxy(ModuleProxy):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def material_package_importable_name(self):
        return self.parent_package_importable_name

    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    @property
    def material_underscored_name(self):
        return self.module_importable_name.split('.')[-2]

    @property
    def materials_package_importable_name(self):
        return '.'.join(self.parent_package_importable_name.split('.')[:-1])

    ### PUBLIC METHODS ###

    def unimport_material_package(self):
        self.remove_package_importable_name_from_sys_modules(self.material_package_importable_name)

    def unimport_materials_package(self):
        self.remove_package_importable_name_from_sys_modules(self.materials_package_importable_name)
