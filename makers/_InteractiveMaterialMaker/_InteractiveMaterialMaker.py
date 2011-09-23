from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
import os


class _InteractiveMaterialMaker(_MaterialPackageMaker):
    '''Interactive material-maker base class.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC METHODS ###

    def write_material_to_disk(self, user_input_pairs, lilypond_score):
        material_package_directory = self.get_new_material_package_directory_from_user()
        print material_package_directory
        os.mkdir(material_package_directory)
        initializer = file(os.path.join(material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.close()
        user_input_lines = self.format_user_input(user_input_pairs)
        input_file = file(os.path.join(material_package_directory, 'input.py'), 'w')
        for line in user_input_lines:
            input_file.write(line + '\n')
        input_file.write('\n')
        for line in self.get_primary_input_lines(user_input_pairs):
            input_file.write(line + '\n')
        input_file.close()
