from baca.scf.BasicModuleProxy import BasicModuleProxy
from baca.scf.helpers import safe_import


class OutputMaterialModuleProxy(BasicModuleProxy):

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
            source_parent_module_importable_name=self.parent_module_importable_name)
