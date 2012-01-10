from baca.scf.MaterialProxy import MaterialProxy
import os


class StaticMaterialProxy(MaterialProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    ### PUBLIC METHODS ###

    def create(self, has_score_builder=True):
        if os.path.exists(self.directory_name):
            line = 'directory {!r} already exists.'.format(self.directory_name)
            self.conditionally_display_lines([line, ''])
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
        if has_score_builder:
            score_builder = file(self.score_builder_file_name, 'w')
            score_builder.write('from abjad import *\n')
            score_builder.write('from abjad.tools import layouttools\n')
            score_builder.write('from output import *\n')
            score_builder.write('\n\n')
            score_builder.write('lilypond_file = None\n')
            score_builder.close()

    def create_interactively(self):
        self.conditionally_clear_terminal()
        materials_package_importable_name = self.get_materials_package_importable_name()
        package_short_name = self.get_package_short_name_of_new_material_interactively()
        has_score_builder = self.get_score_builder_status_of_new_material_package_interactively()
        package_importable_name = '{}.{}'.format(materials_package_importable_name, package_short_name)
        self.create_static_material_package(package_importable_name, has_score_builder)
        self.proceed()
