from baca.scf.MaterialProxy import MaterialProxy
import os


class MakerProxy(MaterialProxy):

    def __init__(self, client_material_package_importable_name, session=None):
        package_importable_name = '{}.{}'.format(self.makers_package_importable_name, self.class_name)
        MaterialProxy.__init__(self, package_importable_name=package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
#    @property
#    def generic_output_name(self):
#        return self._generic_output_name

#    @property
#    def stylesheet_file_name(self):
#        return os.path.join(self.directory_name, 'stylesheet.ly')
