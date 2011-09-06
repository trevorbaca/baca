from baca.scf.SCFProxyObject import SCFProxyObject
import os


class MaterialPackageProxy(SCFProxyObject):

    def __init__(self, score_package_name, material_name):
        self.score_package_name = score_package_name
        self.material_name = material_name
        self.material_directory = os.path.join(
            os.environ.get('SCORES'), score_package_name, 'mus', 'materials', material_name)
        self.material_input_code = os.path.join(
            self.material_directory, '%s_input_code.py' % material_name)
        self.material_output_data_file = os.path.join(
            self.material_directory, '%s_output_data.py' % material_name)
        self.material_pdf = os.path.join(self.material_directory, '%s.pdf' % material_name)
        self.material_ly = os.path.join(self.material_directory, '%s.ly' % material_name)
        self.current_directory = self.material_directory
        self.parent_directory = os.path.dirname(self.current_directory)
        self.parent_initializer = os.path.join(self.parent_directory, '__init__.py')

    ## OVERLOADS ##

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.material_name)

    ## PUBLIC ATTRIBUTES ##

    @property
    def has_output_data(self):
        if os.stat(self.material_output_data_file):
            file_pointer = file(self.material_output_data_file, 'r')
            return bool(file_pointer.readlines())
        return False

    @property
    def output_data(self):
        return self.get_material_output_data()

    ## PUBLIC METHODS ##

    def edit_material_input_code(self):
        material = os.path.join(self.material_directory)
        command = 'vi %s' % self.material_input_code
        os.system(command)

    def exec_statement(self):
        statement = raw_input('xcf: ')
        exec('from abjad import *')
        exec('result = %s' % statement)
        return result

    def get_material_output_data(self):
        if self.has_output_data:
            exec('from %s.mus.materials import %s' % (self.score_package_name, self.material_name))
            exec('result = %s' % self.material_name)
            return result
        else:
            print 'No data available.'

    def open_material_pdf(self):
        command = 'open %s' % self.material_pdf
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
            named_pairs = [('d', 'data'), ('i', 'input'), ('p', 'pdf'), 
                ('r', 'rename'), ('w', 'write'), ('x', 'exec')]
            letter, action = self.present_menu(
                named_pairs = named_pairs, show_options = first_pass)
            if letter == 'b':
                break
            if letter == 'd':
                result = self.get_material_output_data()
                if result:
                    print result
                print ''
            elif letter == 'i':
                self.edit_material_input_code()
            elif letter == 'p':
                self.open_material_pdf()
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
            first_pass = False

    def write_material_to_disk(self):
        command = 'from %s.mus.materials.%s.%s_input_code import %s' % (
            self.score_package_name, self.material_name, self.material_name, self.material_name)
        exec(command)
        exec('_material = %s' % self.material_name)
        output_line = '%s = %r' % (self.material_name, _material)
        output_file = file(self.material_output_data_file, 'w')
        output_file.write(output_line)
        output_file.close()
        print 'Output written to %s_output_data.py.' % self.material_name
        import_statement = 'from %s import %s\n' % (self.material_name, self.material_name)
        file_pointer = file(self.parent_initializer, 'r')
        parent_initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        parent_initializer_lines.add(import_statement)
        parent_initializer_lines = list(parent_initializer_lines)
        parent_initializer_lines.sort()
        file_pointer = file(self.parent_initializer, 'w')
        file_pointer.write(''.join(parent_initializer_lines))
        file_pointer.close()
        print 'Import statement added to materials initializer.'
