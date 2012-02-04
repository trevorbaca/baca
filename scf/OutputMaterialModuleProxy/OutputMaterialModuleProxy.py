from baca.scf.BasicModuleProxy import BasicModuleProxy
from baca.scf.helpers import safe_import


class OutputMaterialModuleProxy(BasicModuleProxy):

    #def __init__(self, module_importable_name, session=None):
    #    BasicModuleProxy.__init__(self, module_importable_name, session=session)

    ### PUBLIC METHODS ###

    def display_output_material(self):
        output_material = self.import_output_material()
        self.display([repr(output_material), ''], capitalize_first_character=False)
        self.session.hide_next_redraw = True
        
    # note that this might have to be reimplement with exec() but seems to work for now
    def import_output_material(self):
        self.unimport_materials_package()
        self.unimport_material_package()
        self.unimport()
        return safe_import(locals(), self.module_short_name, self.material_underscored_name,
            source_parent_package_importable_name=self.parent_package_importable_name)

    def remove(self, prompt=True):
        import baca
        parent_package_initializer = baca.scf.InitializerFileProxy(self.parent_package_initializer_file_name)
        parent_package_initializer.remove_protected_import_statement(
            'output_material', self.material_underscored_name)
        grandparent_package_initializer = baca.scf.InitializerFileProxy(
            self.grandparent_package_initializer_file_name)
        grandparent_package_initializer.remove_protected_import_statement(
            self.material_underscored_name, self.material_underscored_name)
        BasicModuleProxy.remove(self, prompt=prompt)
