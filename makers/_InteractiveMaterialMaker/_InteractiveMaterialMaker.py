from abjad.tools import iotools
from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
import os


class _InteractiveMaterialMaker(_MaterialPackageMaker):
    '''Interactive material-maker base class.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    # TODO: implement this
    def _add_line_to_materials_initializer(self):
        material_name = os.path.basename(self.material_package_directory)

    def _write_initializer_to_disk(self):
        initializer = file(os.path.join(self.material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.close()

    def _write_input_file_to_disk(self, user_input_import_statements, user_input_pairs):
        user_input_lines = self.format_user_input(user_input_pairs)
        input_file = file(os.path.join(self.material_package_directory, 'input.py'), 'w')
        for line in user_input_import_statements:
            input_file.write(line + '\n')
        if user_input_import_statements:
            input_file.write('\n\n')
        for line in user_input_lines:
            input_file.write(line + '\n')
        input_file.write('\n')
        material_name = os.path.basename(self.material_package_directory)
        for line in self.get_primary_input_lines(user_input_pairs, material_name):
            input_file.write(line + '\n')
        input_file.close()

    def _write_output_file_to_disk(self, material):
        output_file = file(os.path.join(self.material_package_directory, 'output.py'), 'w')
        output_file_import_statements = self.get_output_file_import_statements()
        for line in output_file_import_statements:
            output_file.write(line + '\n')
        if output_file_import_statements:
            output_file.write('\n\n')
        material_name = os.path.basename(self.material_package_directory)
        output_file_lines = self.get_output_file_lines(material, material_name)
        for line in output_file_lines:
            output_file.write(line + '\n')
        output_file.close()

    ### PUBLIC METHODS ###

    def write_material_to_disk(self, 
        user_input_import_statements, user_input_pairs, material, lilypond_score):
        self.material_package_directory = self.get_new_material_package_directory_from_user()
        os.mkdir(self.material_package_directory)
        self._write_initializer_to_disk()
        self._write_input_file_to_disk(user_input_import_statements, user_input_pairs)
        self._write_output_file_to_disk(material)
        ly_file = os.path.join(self.material_package_directory, 'visualization.ly')
        iotools.write_expr_to_ly(lilypond_score, ly_file, print_status = False)
        pdf = os.path.join(self.material_package_directory, 'visualization.pdf')
        iotools.write_expr_to_pdf(lilypond_score, pdf, print_status = False)
        #self._add_line_to_materials_initializer()
