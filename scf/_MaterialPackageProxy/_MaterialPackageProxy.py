from abjad.tools import iotools
from baca.scf.PackageProxy import PackageProxy
import os
import subprocess
import sys


class _MaterialPackageProxy(PackageProxy):

    def __init__(self, importable_module_name):
        PackageProxy.__init__(self, importable_module_name)
        self.input_file = os.path.join(self.directory, 'input.py')
        self.output_file = os.path.join(self.directory, 'output.py')
        self.visualizer = os.path.join(self.directory, 'visualization.py')
        self.pdf = os.path.join(self.directory, 'visualization.pdf')
        self.ly = os.path.join(self.directory, 'visualization.ly')
        self.stylesheet = os.path.join(self.directory, 'stylesheet.ly')
        self.input_module_name = '%s.input' % self.importable_module_name
        self.output_module_name = '%s.output' % self.importable_module_name
        self.visualization_module_name = '%s.visualization' % self.importable_module_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def has_input_data(self):
        return bool(self.import_material_from_input_file())

    @property
    def has_input_file(self):
        return os.path.exists(self.input_file)

    @property
    def has_ly(self):
        return os.path.exists(self.ly)

    @property
    def has_output_data(self):
        return bool(self.import_material_from_output_file())

    @property
    def has_output_file(self):
        return os.path.exists(self.output_file)

    @property
    def has_pdf(self):
        return os.path.exists(self.pdf)

    @property
    def has_score_definition(self):
        return bool(self.import_score_definition_from_visualizer())

    @property
    def has_stylesheet(self):
        return os.path.exists(self.stylesheet)
    
    @property
    def has_visualizer(self):
        return os.path.exists(self.visualizer)

    @property
    def help_item_width(self):
        return 5

    @property
    def is_in_score(self):
        return not self.is_shared        

    @property
    def is_interactive(self):
        return bool(self.has_tag('maker'))

    @property
    def is_shared(self):
        return bool(self.importable_module_name.startswith('baca'))

    @property
    def is_static(self):
        return not self.is_interactive

    @property
    def materials_module_name(self):
        if self.score_package_name is None:
            return 'baca.materials'
        else:
            return '%s.mus.materials' % self.score_package_name

    @property
    def module_name(self):
        return self.importable_module_name.split('.')[-1]

    @property
    def score_package_name(self):
        if self.importable_module_name.startswith('baca'):
            return None
        else:
            return self.importable_module_name.split('.')[0]

    @property
    def spaced_material_name(self):
        return self.module_name.replace('_', ' ')

    @property
    def underscored_material_name(self):
        return self.module_name

    @property
    def user_input_wrapper(self):
        exec('from %s import user_input' % self.input_module_name)
        return user_input

    ### PUBLIC METHODS ###

    def add_material_to_materials_initializer(self):
        import_statement = 'from %s import %s\n' % (self.material_name, self.material_name)
        parent_package = PackageProxy(self.parent_directory)
        parent_package.add_line_to_initializer(import_statement)

    def create_ly_and_pdf_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_ly(lilypond_file, self.ly)
            iotools.write_expr_to_pdf(lilypond_file, self.pdf)
        else:
            print 'LilyPond file is the same. (LilyPond file and PDF preserved.)'
        print ''
        
    def create_ly_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_ly(lilypond_file, self.ly)
        else:
            print 'LilyPond file is the same. (LilyPond file preserved.)'
        print ''

    def create_pdf_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_pdf(lilypond_file, self.pdf)
        else:
            print 'LilyPond file is the same. (PDF preserved.)'
        print ''

    def create_visualizer(self):
        file_pointer = file(self.visualizer, 'w')
        file_pointer.write('from abjad import *\n')
        file_pointer.write('from abjad.tools import layouttools\n')
        line = 'from output import %s\n' % self.material_name
        file_pointer.write(line)
        file_pointer.write('\n\n\n')
        file_pointer.close()
        self.edit_visualizer()

    def delete_material(self):
        self.remove_material_from_materials_initializer()
        result = self.remove_directory()
        if result:
            self.proceed()

    def edit_initializer(self):
        os.system('vi %s' % self.initializer)

    def edit_input_file(self):
        os.system('vi + %s' % self.input_file)

    def edit_ly(self):
        os.system('vi %s' % self.ly)

    def edit_output_file(self):
        os.system('vi + %s' % self.output_file)

    def edit_stylesheet(self):
        os.system('vi %s' % self.stylesheet)

    def edit_visualizer(self):
        os.system('vi + %s' % self.visualizer)

    def import_attribute_from_input_file(self, attribute_name):
        try:
            exec('from %s import %s' % (self.input_module_name, attribute_name))
            exec('result = %s' % attribute_name)
            return result
        except ImportError:
            return None

    def import_material_from_input_file(self):
        self.unimport_input_module()
        try:
            exec('from %s import %s' % (self.input_module_name, self.material_name))
            exec('result = %s' % self.material_name)
            return result
        except ImportError as e:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')
    
    def import_material_from_output_file(self):
        self.unimport_output_module_hierarchy()
        try:
            exec('from %s import %s' % (self.output_module_name, self.material_name))
            exec('result = %s' % self.material_name)
            return result
        except ImportError as e:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')

    def import_score_definition_from_visualizer(self):
        if not self.has_visualizer:
            return None
        self.unimport_visualization_module()
        self.unimport_output_module()
        command = 'from %s import lilypond_file' % self.visualization_module_name 
        exec(command)
        return lilypond_file
        
    def get_output_preamble_lines(self):
        self.unimport_input_module()
        command = 'from %s import output_preamble_lines' % self.input_module_name
        try:
            exec(command)
            # keep list from persisting between multiple calls to this method
            output_preamble_lines = list(output_preamble_lines)
            output_preamble_lines.append('\n')
        except ImportError:
            output_preamble_lines = []
        return output_preamble_lines

    def lilypond_file_format_is_equal_to_visualizer_ly(self, lilypond_file):
        temp_ly_file = os.path.join(os.environ.get('HOME'), 'tmp.ly')
        iotools.write_expr_to_ly(lilypond_file, temp_ly_file, print_status=False)
        trimmed_temp_ly_file_lines = self.trim_ly_lines(temp_ly_file)
        os.remove(temp_ly_file)
        trimmed_visualizer_ly_lines = self.trim_ly_lines(self.ly)
        return trimmed_temp_ly_file_lines == trimmed_visualizer_ly_lines

    def manage_input(self, command_string):
        if command_string == 'i':
            self.edit_input_file()
        elif command_string == 'id':
            print repr(self.import_material_from_input_file())
            print ''
        elif command_string == 'ih':
            print '%s: edit input file' % 'i'.rjust(self.help_item_width)
            print '%s: display input data' % 'id'.rjust(self.help_item_width)
            print '%s: edit input file and run abjad on input file' % 'ij'.rjust(self.help_item_width)
            print '%s: write input data to output file.' % 'iw'.rjust(self.help_item_width)
            print ''
        elif command_string == 'ij':
            self.edit_input_file()
            self.run_abjad_on_input_file()
        elif command_string == 'iw':
            self.write_input_data_to_output_file(is_forced=True)
            print ''

    def manage_ly(self, command_string):
        if command_string == 'l':
            if self.has_ly:
                self.edit_ly()
            elif self.has_visualizer:
                if self.query('Create LilyPond file from visualizer? '):
                    self.create_ly_from_visualizer()    
                print ''
            elif self.has_output_data:
                print "Data exists but visualizer doesn't.\n"
                if self.query('Create visualizer? '):
                    self.create_visualizer()
                print ''
            elif self.has_input_file:
                if self.query('Write material to disk? '):
                    self.write_input_data_to_output_file(is_forced=True)
                print ''
            else:
                if self.query('Create input file? '):
                    self.edit_input_file()
                print ''
        elif command_string == 'lw':
            self.create_ly_from_visualizer(is_forced=True)
        elif command_string == 'lwo':
            self.create_ly_from_visualizer(is_forced=True)
            self.edit_ly()
        elif command_string == 'lh':
            print '%s: open ly' % 'l'.rjust(self.help_item_width)
            print '%s: write ly' % 'lw'.rjust(self.help_item_width)
            print '%s: write ly and open' % 'lwo'.rjust(self.help_item_width)
            print ''

    def manage_material(self, menu_header=None):
        from baca.scf.MenuSpecifier import MenuSpecifier
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_header = menu_header
            menu_specifier.menu_body = self.spaced_material_name
            if self.is_interactive:
                menu_specifier.sentence_length_items.append(('k', 'reload user input'))
            menu_specifier.named_pairs.append(('i', 'input'))
            menu_specifier.named_pairs.append(('o', 'output'))
            if self.has_visualizer:
                menu_specifier.named_pairs.append(('v', 'visualizer'))
            if self.has_ly:
                menu_specifier.named_pairs.append(('l', 'ly'))
            if self.has_stylesheet:
                menu_specifier.named_pairs.append(('y', 'stylesheet'))
            if self.has_pdf:
                menu_specifier.named_pairs.append(('p', 'pdf'))
            menu_specifier.named_pairs.append(('n', 'initializer'))
            menu_specifier.secondary_named_pairs.append(('d', 'delete'))
            menu_specifier.secondary_named_pairs.append(('g', 'get tag'))
            menu_specifier.secondary_named_pairs.append(('r', 'rename'))
            menu_specifier.secondary_named_pairs.append(('s', 'summarize'))
            menu_specifier.secondary_named_pairs.append(('t', 'tags'))
            menu_specifier.secondary_named_pairs.append(('z', 'regenerate'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'd':
                self.delete_material()
                break
            elif key == 'i':
                self.manage_input(key)
            elif key == 'k':
                self.reload_user_input()
            elif key == 'l':
                self.manage_ly(key)
            elif key == 'n':
                self.edit_initializer()
            elif key == 'o':
                self.manage_output(key)
            elif key == 'p':
                self.manage_pdf(key)
            elif key == 'r':
                self.rename_material()
            elif key == 's':
                self.summarize_material()
            elif key == 't':
                self.manage_tags(menu_header=menu_specifier.menu_title)
            elif key == 'v':
                self.manage_visualizer(key)
            elif key == 'y':
                self.edit_stylesheet()
            elif key == 'z':
                self.manage_regeneration(key)

    def manage_output(self, command_string):
        if command_string == 'o':
            self.edit_output_file()
        elif command_string == 'od':
            print repr(self.import_material_from_output_file())
            print ''
        elif command_string == 'oh':
            print '%s: open output file' % 'o'.rjust(self.help_item_width)
            print '%s: display output data' % 'od'.rjust(self.help_item_width)
            print ''

    def manage_pdf(self, command_string):
        if command_string == 'p':
            if self.has_pdf:
                self.open_pdf()
            elif self.has_visualizer:
                if self.query('Create PDF from visualizer? '):
                    self.create_pdf_from_visualizer()
                print ''
            elif self.has_output_data:
                print "Data exists but visualizer doesn't.\n"
                if self.query('Create visualizer? '):
                    self.create_visualizer()
                print ''
            elif self.has_input_file:
                if self.query('Write material to disk? '):
                    self.write_input_data_to_output_file(is_forced=True)
                print ''
            else:
                if self.query('Create input file? '):
                    self.edit_input_file()
                print '' 
        elif command_string == 'pw':
            self.create_pdf_from_visualizer(is_forced=True)
        elif command_string == 'pwo':
            self.create_pdf_from_visualizer(is_forced=True)
            self.open_pdf()
        elif command_string == 'ph':
            print '%s: open pdf' % 'p'.rjust(self.help_item_width)
            print '%s: write pdf ' % 'pw'.rjust(self.help_item_width)
            print '%s: write pdf and open' % 'pwo'.rjust(self.help_item_width)
            print ''

    def manage_regeneration(self, command_string):
        if command_string == 'z':
            self.regenerate_everything(is_forced=True)
        elif command_string == 'zh':
            print '%s: regenerate everything' % 'z'.rjust(self.help_item_width)
            print '%s: regenerate everything and open pdf' % 'zo'.rjust(self.help_item_width)
            print ''
        elif command_string == 'zo':
            self.regenerate_everything(is_forced=True)
            self.open_pdf()

    def manage_visualizer(self, command_string):
        if self.has_visualizer:
            if command_string == 'v':
                self.edit_visualizer()
            elif command_string == 'vh':
                print '%s: edit visualizer' % 'v'.rjust(self.help_item_width)
                print '%s: edit visualizer and run abjad on visualizer' % 'vj'.rjust(self.help_item_width)
                print '%s: run abjad on visualizer' % 'vjj'.rjust(self.help_item_width)
                print ''
            elif command_string == 'vj':
                self.edit_visualizer()
                self.run_abjad_on_visualizer()
            elif command_string == 'vjj':
                self.run_abjad_on_visualizer()
        elif self.has_output_data:
            print "Data exists but visualizer doesn't.\n"
            if self.query('Create visualizer? '):
                self.create_visualizer()
        elif self.has_input_file:
            if self.query('Write material to disk? '):
                self.write_input_data_to_output_file(is_forced=True)
        else:
            if self.query('Create input file? '):
                self.edit_input_file()

    def open_pdf(self):
        command = 'open %s' % self.pdf
        os.system(command)

    def overwrite_output_file(self):
        output_file = file(self.output_file, 'w')
        output_line = '%s = None\n' % self.material_name
        output_file.write(output_line)
        output_file.close()

    def prepend_score_package_name(self, material_name):
        if not material_name.startswith(self.score_package_name + '_'):
            material_name = '%s_%s' % (self.score_package_name, material_name)
        return material_name

    def regenerate_everything(self, is_forced=False):
        is_changed = self.write_input_data_to_output_file(is_forced=is_forced)
        is_changed = self.create_ly_and_pdf_from_visualizer(is_forced=(is_changed or is_forced))
        return is_changed

    def reload_user_input(self):
        maker = self.import_attribute_from_input_file('maker')
        maker.materials_directory = self.directory
        user_input_wrapper = self.import_attribute_from_input_file('user_input')
        maker.edit_interactively(user_input_wrapper, score_title=self.score_title)

    def rename_material(self):
        print 'Current material name: %s' % self.material_name
        new_material_name = raw_input('New material name:     ')
        print ''
        new_material_name = self.prepend_score_package_name(new_material_name)
        print 'Current material name: %s' % self.material_name
        print 'New material name:     %s' % new_material_name
        print ''
        if not self.confirm():
            return
        print ''
        if self.is_in_repository:
            # update parent initializer
            self.globally_replace_in_file(self.parent_initializer, self.material_name, new_material_name)
            # rename package directory
            new_directory = self.directory.replace(self.material_name, new_material_name)
            command = 'svn mv %s %s' % (self.directory, new_directory)
            os.system(command)
            # update package initializer
            new_package_directory = os.path.join(self.parent_directory, new_material_name)
            new_initializer = os.path.join(new_package_directory, '__init__.py')
            self.globally_replace_in_file(new_initializer, self.material_name, new_material_name)
            # rename files in package
            for old_file_name in os.listdir(new_package_directory):
                if not old_file_name.startswith(('.', '_')):
                    old_path_name = os.path.join(new_package_directory, old_file_name)
                    new_path_name = old_path_name.replace(self.material_name, new_material_name)
                    command = 'svn mv %s %s' % (old_path_name, new_path_name)
                    os.system(command)
            # rename output data
            new_output_data = os.path.join(new_package_directory, 'output.py')
            self.globally_replace_in_file(new_output_data, self.material_name, new_material_name)
            print ''
            # commit
            commit_message = 'Renamed %s to %s.' % (self.material_name, new_material_name)
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m "%s" %s' % (commit_message, self.parent_directory)
            os.system(command)
            print ''
        else:
            raise NotImplementedError('commit to repository and then rename.')

    def remove_line_from_initializer(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == line]
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def remove_material_from_materials_initializer(self):
        import_statement = 'from %s import %s\n' % (self.material_name, self.material_name)
        self.remove_line_from_initializer(self.parent_initializer, import_statement)

    def reveal_modules(self):
        exec('module_names = sys.modules.keys()')
        module_names = [x for x in module_names if x.startswith(self.score_package_name)]
        module_names.sort()
        return module_names

    def run_abjad_on_input_file(self):
        os.system('abjad %s' % self.input_file)
        print ''

    def run_abjad_on_visualizer(self):
        os.system('abjad %s' % self.visualizer)
        print ''

    def summarize_material(self):
        found = []
        missing = []
        artifact_name = 'input file'
        if self.has_input_file:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'input data'
        if self.has_input_data:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'ouput file'
        if self.has_output_file:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'output data'
        if self.has_output_data:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'visualizer'
        if self.has_visualizer:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'score definition'
        if self.has_score_definition:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'ly'
        if self.has_ly:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'pdf'
        if self.has_pdf:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        if found:
            print 'Found %s.' % ', '.join(found)
        if missing:
            print 'Missing %s.' % ', '.join(missing)
        print ''
        
    def trim_ly_lines(self, ly_file_name):
        '''Remove "Abjad revision 4776" and "2011-09-13 18:33" lines.
        '''
        trimmed_ly_lines = []
        file_pointer = file(ly_file_name, 'r')
        found_version_command = False
        for line in file_pointer.readlines():
            if found_version_command:
                trimmed_ly_lines.append(line)
            if line.startswith(r'\version'):
                found_version_command = True
        trimmed_ly_content = ''.join(trimmed_ly_lines)
        return trimmed_ly_content

    def unimport_input_module(self):
        self.remove_module_name_from_sys_modules(self.input_module_name)

    def unimport_material_module(self):
        self.remove_module_name_from_sys_modules(self.importable_module_name)

    def unimport_materials_module(self):
        self.remove_module_name_from_sys_modules(self.materials_module_name)

    def unimport_output_module(self):
        self.remove_module_name_from_sys_modules(self.output_module_name)

    def unimport_output_module_hierarchy(self):
        self.unimport_materials_module()
        self.unimport_material_module()
        self.unimport_output_module()

    def unimport_score_package(self):
        self.remove_module_name_from_sys_modules(self.score_package_name)

    def unimport_visualization_module(self):
        self.remove_module_name_from_sys_modules(self.visualization_module_name)

    def _write_input_data_to_output_file(self):
        self.remove_material_from_materials_initializer()
        self.overwrite_output_file()
        output_file = file(self.output_file, 'w')
        output_preamble_lines = self.get_output_preamble_lines()
        if output_preamble_lines:
            output_file.write('\n'.join(output_preamble_lines))
        input_data = self.import_material_from_input_file()
        output_line = '%s = %r' % (self.material_name, input_data)
        output_file.write(output_line)
        output_file.close()
        self.add_material_to_materials_initializer()
        print "Material in 'input.py' written to 'output.py' ..."

    def write_input_data_to_output_file(self, is_forced=False):
        is_changed = self.import_material_from_input_file() != self.import_material_from_output_file()
        if is_changed or is_forced:
            self._write_input_data_to_output_file()
        else:
            print 'Input data equals output data. (Output data preserved.)'
        return is_changed
