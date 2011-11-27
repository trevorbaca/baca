from baca.scf.MaterialProxy import MaterialProxy
import os


class StaticMaterialProxy(MaterialProxy):

    ### PUBLIC ATTRIBUTES ###


    ### PUBLIC METHODS ###

    def create(self, has_visualizer=True):
        if os.path.exists(self.directory_name):
            print 'Directory {!r} already exists.'.format(self.directory_name)
            return False
        os.mkdir(self.directory_name)
        initializer = file(self.initializer_file_name, 'w')
        initializer.write('from output import *\n')
        initializer.close()
        input_file = file(self.input_file_name, 'w')
        input_file.write('{} = None\n'.format(self.package_short_name))
        input_file.write('output_preamble_lines = []\n')
        input_file.write('')
        input_file.close()
        output_file = file(self.output_file_name, 'w')
        output_file.write('{} = None\n'.format(self.package_short_name))
        output_file.write('')
        output_file.close()
        if has_visualizer:
            visualizer = file(self.visualizer_file_name, 'w')
            visualizer.write('from abjad import *\n')
            visualizer.write('from abjad.tools import layouttools\n')
            visualizer.write('from output import *\n')
            visualizer.write('\n\n')
            visualizer.write('lilypond_file = None\n')
            visualizer.close()

    def create_interactively(self):
        self.conditionally_clear_terminal()
        materials_package_importable_name = self.get_materials_package_importable_name()
        package_short_name = self.get_package_short_name_of_new_material_interactively()
        has_visualizer = self.get_visualizer_status_of_new_material_package_interactively()
        package_importable_name = '{}.{}'.format(materials_package_importable_name, package_short_name)
        self.create_static_material_package(package_importable_name, has_visualizer)
        self.proceed()
