from baca.scf._MaterialProxy import _MaterialProxy
import os


class StaticMaterialProxy(_MaterialProxy):

    ### PUBLIC ATTRIBUTES ###


    ### PUBLIC METHODS ###

    def create(self, has_visualizer=True):
        if os.path.exists(self.directory_name):
            print 'Directory %r already exists.' % self.directory_name
            return False
        os.mkdir(self.directory_name)
        initializer = file(self.initializer_file_name, 'w')
        initializer.write('from output import *\n')
        initializer.close()
        input_file = file(self.input_file_name, 'w')
        input_file.write('%s = None\n' % self.package_short_name)
        input_file.write('output_preamble_lines = []\n')
        input_file.write('')
        input_file.close()
        output_file = file(self.output_file_name, 'w')
        output_file.write('%s = None\n' % self.package_short_name)
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

    def create_interactively(self, menu_header=None):
        self.clear_terminal()
        menu_body = 'create static material package'
        menu_title = self.make_menu_title(menu_header, menu_body)
        materials_package_importable_name = self.get_materials_package_importable_name(
            menu_header=menu_title)
        package_short_name = self.get_package_short_name_of_new_material_interactively(menu_header)
        has_visualizer = self.get_visualizer_status_of_new_material_package_interactively()
        package_importable_name = '%s.%s' % (materials_package_importable_name, package_short_name)
        self.create_static_material_package(package_importable_name, has_visualizer)
        self.proceed()
