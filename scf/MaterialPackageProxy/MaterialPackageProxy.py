from baca.scf.SCFProxyObject import SCFProxyObject
import os
import sys


class MaterialPackageProxy(SCFProxyObject):

    def __init__(self, score_package_name, material_name):
        self.score_package_name = score_package_name
        self.material_name_with_spaces = material_name
        material_name = material_name.replace(' ', '_')
        self.material_name = material_name
        self.underscored_material_name = self.material_name.replace(' ', '_')
        self.directory = os.path.join(os.environ.get('SCORES'), score_package_name)
        self.directory = os.path.join(self.directory, 'mus', 'materials', self.underscored_material_name)
        self.input_file = os.path.join(self.directory, '%s_input.py' % self.underscored_material_name)
        self.output_file = os.path.join(self.directory, '%s_output.py' % self.underscored_material_name)
        self.visualizer = os.path.join(self.directory, '%s_visualizer.py' % self.underscored_material_name)
        self.pdf = os.path.join(self.directory, '%s.pdf' % self.underscored_material_name)
        self.ly = os.path.join(self.directory, '%s.ly' % self.underscored_material_name)
        self.input_module_name = '%s.mus.materials.%s.%s_input'
        self.input_module_name %= self.score_package_name, self.material_name, self.material_name
        self.material_module_name = '%s.mus.materials.%s' % (self.score_package_name, self.material_name)
        self.materials_module_name = '%s.mus.materials' % self.score_package_name
        self.output_module_name = '%s.mus.materials.%s.%s_output'
        self.output_module_name %= self.score_package_name, self.material_name, self.material_name
        self.visualizer_module_name = '%s.%s_visualizer' % (self.material_module_name, self.material_name)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.material_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def has_input_file(self):
        return os.path.exists(self.input_file)

    @property
    def has_ly(self):
        return os.path.exists(self.ly)

    @property
    def has_output_data(self):
        if os.path.exists(self.output_file):
            file_pointer = file(self.output_file, 'r')
            return bool(file_pointer.readlines())
        return False

    @property
    def has_pdf(self):
        return os.path.exists(self.pdf)
    
    @property
    def has_visualizer(self):
        return os.path.exists(self.visualizer)

    @property
    def input_file_has_complete_material_definition(self):
        try:
            input_data = self.import_material_from_input_file()
            return True
        except ImportError:
            return False

    @property
    def output_data(self):
        return self.import_material_from_output_file()

    ### PUBLIC METHODS ###

    def add_line_to_initializer(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def add_material_to_materials_initializer(self):
        import_statement = 'from %s import %s\n' % (self.material_name, self.material_name)
        self.add_line_to_initializer(self.parent_initializer, import_statement)

    def create_ly(self):
        self.print_not_implemented()

    def create_pdf(self):
        self.print_not_implemented() 

    def create_visualizer(self):
        if not self.has_output_data:
            # this needs to be filled in with something that exists
            pass
        file_pointer = file(self.visualizer, 'w')
        file_pointer.write('from abjad import *\n')
        line = 'from %s_output import %s\n' % (self.material_name, self.material_name)
        file_pointer.write(line)
        file_pointer.write('\n\n\n')
        file_pointer.close()
        self.edit_visualizer()

    def edit_input_file(self):
        command = 'vi + %s' % self.input_file
        os.system('vi + %s' % self.input_file)

    def edit_output_file(self):
        os.system('vi + %s' % self.output_file)

    def edit_visualizer(self):
        os.system('vi + %s' % self.visualizer)

    def import_material_from_input_file(self):
        self.unimport_input_module()
        try:
            command = 'from %s import %s' % (self.input_module_name, self.material_name)
            exec(command)
            exec('result = %s' % self.material_name)
            return result
        except ImportError:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')
    
    def import_lily_pond_file_object_from_visualizer(self):
        #print 'Importing LilyPond file object from visualizer ...'
        self.unimport_visualizer_module()
        command = 'from %s import lily_file' % self.visualizer_module_name 
        exec(command)
        return lily_file
        
    def import_material_from_output_file(self):
        self.unimport_output_module_hierarchy()
        try:
            exec('from %s.mus.materials import %s' % (self.score_package_name, self.material_name))
            exec('result = %s' % self.material_name)
            return result
        except ImportError as e:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')

    def get_output_preamble_lines(self):
        self.unimport_input_module()
        command = 'from %s.mus.materials.%s.%s_input import output_preamble_lines'
        command %= self.score_package_name, self.material_name, self.material_name
        try:
            exec(command)
            # to keep list from persisting between multiple calls to this method
            output_preamble_lines = list(output_preamble_lines)
            output_preamble_lines.append('\n')
        except ImportError:
            output_preamble_lines = []
        return output_preamble_lines

    def manage_material(self):
        is_first_pass = True
        while True:
            is_redraw = False
            if is_first_pass:
                self.print_menu_title('%s - %s' % (
                    self.score_title, self.material_name.replace('_', ' ')))
            named_pairs = [
                ('i', 'input'), 
                ('o', 'output'), 
                ('p', 'pdf'), 
                ('r', 'rename'), 
                ('v', 'visualizer'), 
                ('y', 'ly'),
                ('z', 'regenerate'),
                ]
            kwargs = {'named_pairs': named_pairs, 'show_options': is_first_pass}
            command_string, menu_value = self.display_menu(**kwargs)
            key = command_string[0]
            if key == 'b':
                break
            elif key == 'd':
                is_redraw = True
            elif key == 'i':
                if command_string == 'i':
                    self.edit_input_file()
                elif command_string == 'id':
                    print repr(self.import_material_from_input_file())
                    print ''
                elif command_string == 'ih':
                    print '%s: edit input file' % 'i'.rjust(4)
                    print '%s: print input data repr' % 'id'.rjust(4)
                    print '%s: edit input file; run abjad on input file' % 'ij'.rjust(4)
                    print '%s: run abjad on input file' % 'ijj'.rjust(4)
                    print ''
                elif command_string == 'ij':
                    self.edit_input_file()
                    self.run_abjad_on_input_file()
                elif command_string == 'ijj':
                    self.run_abjad_on_input_file()                    
            elif key == 'o':
                if command_string == 'o':
                    self.edit_output_file()
                elif command_string == 'od':
                    print repr(self.import_material_from_output_file())
                    print ''
                elif command_string == 'oh':
                    print '%s: edit output file' % 'o'.rjust(4)
                    print '%s: print output data repr' % 'od'.rjust(4)
                    print '%s: write material to output file' % 'ow'.rjust(4)
                    print ''
                elif command_string == 'ow':
                    self.write_input_data_to_output_file()
                    print ''
            elif key == 'p':
                if command_string == 'p':
                    if self.has_pdf:
                        self.open_pdf()
                    elif self.has_visualizer:
                        if self.query('Create PDF from visualizer? '):
                            self.create_pdf()
                    elif self.has_output_data:
                        print "Data exists but visualizer doesn't.\n"
                        if self.query('Create visualizer? '):
                            self.create_visualizer()
                    elif self.has_input_file:
                        if self.query('Write material to disk? '):
                            self.write_input_data_to_output_file()
                    else:
                        if self.query('Create input file? '):
                            self.edit_input_file()
                elif command_string == 'pc':
                    self.create_pdf()
                elif command_string == 'ph':
                    print '%s: open pdf' % 'p'.rjust(4)
                    print '%s: create pdf from visualizer' % 'pc'.rjust(4)
                    print ''
            elif key == 'q':
                raise SystemExit
            elif key == 'r':
                self.rename_material()
            elif key == 'v':
                if self.has_visualizer:
                    if command_string == 'v':
                        self.edit_visualizer()
                    elif command_string == 'vh':
                        print '%s: edit visualizer' % 'v'.rjust(4)
                        print '%s: edit visualizer; run abjad on visualizer' % 'vj'.rjust(4)
                        print '%s: run abjad on visualizer' % 'vjj'.rjust(4)
                        print '%s: print visualizer lilypond file object repr' % 'vlf'.rjust(4)
                        print ''
                    elif command_string == 'vj':
                        self.edit_visualizer()
                        self.run_abjad_on_visualizer()
                    elif command_string == 'vjj':
                        self.run_abjad_on_visualizer()
                    elif command_string == 'vlf':
                        print repr(self.import_lily_pond_file_object_from_visualizer())
                        print ''
                elif self.has_output_data:
                    print "Data exists but visualizer doesn't.\n"
                    if self.query('Create visualizer? '):
                        self.create_visualizer()
                elif self.has_input_file:
                    if self.query('Write material to disk? '):
                        self.write_input_data_to_output_file()
                else:
                    if self.query('Create input file? '):
                        self.edit_input_file()
            elif key == 'w':
                self.write_input_data_to_output_file()
                print ''
            elif key == 'x':
                self.exec_statement()
            elif key == 'y':
                if self.has_ly:
                    self.open_ly()
                elif self.has_visualizer:
                    if self.query('Create LilyPond file from visualizer? '):
                        self.create_ly()    
                elif self.has_output_data:
                    print "Data exists but visualizer doesn't.\n"
                    if self.query('Create visualizer? '):
                        self.create_visualizer()
                elif self.has_input_file:
                    if self.query('Write material to disk? '):
                        self.write_input_data_to_output_file()
                else:
                    if self.query('Creat input file? '):
                        self.edit_input_file()
            elif key == 'z':
                self.write_input_data_to_output_file_if_necessary()
            if is_redraw:
                is_first_pass = True
            else:
                is_first_pass = False

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

    def rename_material(self):
        print 'current material name: %s' % self.material_name
        new_material_name = raw_input('new material name:     ')
        print ''
        new_material_name = self.prepend_score_package_name(new_material_name)
        print 'current material name: %s' % self.material_name
        print 'new material name:     %s' % new_material_name
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
            new_output_data = '%s_output.py' % new_material_name
            new_output_data = os.path.join(new_package_directory, new_output_data)
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

    def run_abjad_on_visualizer(self):
        os.system('abjad %s' % self.visualizer)

    def unimport_input_module(self):
        self.remove_module_name_from_sys_modules(self.input_module_name)

    def unimport_material_module(self):
        self.remove_module_name_from_sys_modules(self.material_module_name)

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

    def unimport_visualizer_module(self):
        self.remove_module_name_from_sys_modules(self.visualizer_module_name)

    def write_input_data_to_output_file(self):
        self.remove_material_from_materials_initializer()
        self.overwrite_output_file()
        output_file = file(self.output_file, 'w')
        output_preamble_lines = self.get_output_preamble_lines()
        output_file.write('\n'.join(output_preamble_lines))
        input_data = self.import_material_from_input_file()
        output_line = '%s = %r' % (self.material_name, input_data)
        output_file.write(output_line)
        output_file.close()
        self.add_material_to_materials_initializer()
        print 'Output written to %s_output.py.' % self.material_name

    def write_input_data_to_output_file_if_necessary(self):
        if self.import_material_from_input_file() == self.import_material_from_output_file():
            print 'Input data equals output data; no material written to disk.'
        else:
            self.write_input_data_to_output_file()
        print ''
