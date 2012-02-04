from baca.scf.BasicModuleProxy import BasicModuleProxy
from baca.scf.helpers import safe_import
import os


class OutputMaterialModuleProxy(BasicModuleProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def is_faulty(self):
        return not bool(self.import_output_material())

    ### PUBLIC METHODS ###

    def display_output_material(self):
        output_material = self.import_output_material()
        self.display([repr(output_material), ''], capitalize_first_character=False)
        self.session.hide_next_redraw = True
        
    def import_output_material(self):
        # the next two lines actually matter
        self.unimport_materials_package()
        self.unimport_material_package()
        #self.unimport()
        if os.path.exists(self.full_file_name):
            om = open(self.full_file_name, 'r')
            file_contents_string = om.read()
            om.close()
            try:
                exec(file_contents_string)
            except:
                print 'exception raise executing {!r}.'.format(self.full_file_name)
                return
            result = locals().get(self.material_underscored_name)
            return result

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
