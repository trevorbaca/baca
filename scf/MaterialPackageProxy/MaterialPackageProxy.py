from baca.scf.SCFProxyObject import SCFProxyObject
import os


class MaterialPackageProxy(SCFProxyObject):

    def __init__(self, score_package_name, material_name):
        self.score_package_name = score_package_name
        self.material_name = material_name
        self.directory = os.path.join(os.environ.get('SCORES'), score_package_name)
        self.directory = os.path.join(self.directory, 'mus', 'materials', material_name)
        self.input_file = os.path.join(self.directory, '%s_input_code.py' % material_name)
        self.output_file = os.path.join(self.directory, '%s_output_data.py' % material_name)
        self.visualizer = os.path.join(self.directory, '%s_visualizer.py' % material_name)
        self.pdf = os.path.join(self.directory, '%s.pdf' % material_name)
        self.ly = os.path.join(self.directory, '%s.ly' % material_name)

    ## OVERLOADS ##

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.material_name)

    ## PUBLIC ATTRIBUTES ##

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
    def output_data(self):
        return self.get_output_data()

    ## PUBLIC METHODS ##

    def create_ly(self):
        self.print_not_implemented()

    def create_pdf(self):
        self.print_not_implemented() 

    def create_visualizer(self):
        self.print_not_implemented()

    def edit_input_file(self):
        command = 'vi %s' % self.input_file
        os.system(command)

    def edit_output_file(self):
        command = 'vi %s' % self.output_file
        os.system(command)

    def get_output_data(self):
        if self.has_output_data:
            exec('from %s.mus.materials import %s' % (self.score_package_name, self.material_name))
            exec('result = %s' % self.material_name)
            return result
        else:
            print 'No data available.'

    def open_pdf(self):
        command = 'open %s' % self.pdf
        os.system(command)

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
            self.globally_replace_in_file(
                self.parent_initializer, self.material_name, new_material_name)
            # rename package directory
            new_current_directory = self.current_directory.replace(
                self.material_name, new_material_name)
            command = 'svn mv %s %s' % (self.current_directory, new_current_directory)
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
            new_output_data = '%s_output_data.py' % new_material_name
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

    def run_startup_interface(self):
        self.print_menu_title('%s - %s' % (self.score_title, self.material_name))
        first_pass = True
        while True:
            named_pairs = [
                ('i', 'input'), ('o', 'output'), ('p', 'pdf'), ('r', 'rename'), 
                ('v', 'visualizer'), ('w', 'write'), ('y', 'ly')]
            letter, action = self.display_menu(
                named_pairs = named_pairs, show_options = first_pass)
            if letter == 'b':
                break
            if letter == 'i':
                self.edit_input_file()
            elif letter == 'o':
                print 'e: edit  w: write\n'
                response = raw_input('scf> ')
                if response.lower() == 'e':
                    self.edit_output_file()
                elif response.lower() == 'w':
                    self.write_material_to_disk()    
                print ''
            elif letter == 'p':
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
                        self.write_material_to_disk()
                else:
                    if self.query('Creat input file? '):
                        self.edit_input_file()
            elif letter == 'q':
                raise SystemExit
            elif letter == 'r':
                self.rename_material()
            elif letter == 'w':
                self.write_material_to_disk()
                print ''
            elif letter == 'x':
                print self.exec_statement()
                print ''
            elif letter == 'y':
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
                        self.write_material_to_disk()
                else:
                    if self.query('Creat input file? '):
                        self.edit_input_file()
            first_pass = False

    def update_initializer_with_line(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def write_material_to_disk(self):
        command = 'from %s.mus.materials.%s.%s_input_code import %s' % (
            self.score_package_name, self.material_name, self.material_name, self.material_name)
        exec(command)
        exec('_material = %s' % self.material_name)
        output_line = '%s = %r' % (self.material_name, _material)
        output_file = file(self.output_file, 'w')
        output_file.write(output_line)
        output_file.close()
        print 'Output written to %s_output_data.py.' % self.material_name
        import_statement = 'from %s import %s\n' % (self.material_name, self.material_name)
        self.update_initializer_with_line(self.parent_initializer, import_statement)
        print 'Import statement added to materials initializer.'
