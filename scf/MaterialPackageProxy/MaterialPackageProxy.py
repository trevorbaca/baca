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
        self.material_output_data = os.path.join(
            self.material_directory, '%s_output_data.py' % material_name)
        self.material_pdf = os.path.join(self.material_directory, '%s.pdf' % material_name)
        self.material_ly = os.path.join(self.material_directory, '%s.ly' % material_name)
        self.top_level_directory = self.material_directory

    ## OVERLOADS ##

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.material_name)

    ## PUBLIC METHODS ##

    def edit_material_input_code(self):
        material = os.path.join(self.material_directory)
        command = 'vi %s' % self.material_input_code
        os.system(command)

    def exec_statement(self):
        statement = raw_input('statement to exec: ')
        print eval(statement)

    def get_material_output_data(self):
        exec('from %s.mus.materials import %s' % (self.score_package_name, self.material_name))
        exec('result = %s' % self.material_name)
        return result

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
            command = 'svn mv %s %s' % (self.material_name, new_material_name)
            print command
            #os.system(command)

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
                print self.get_material_output_data()
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
                self.exec_statement()
                print ''
            first_pass = False

    def write_material_to_disk(self):
        command = 'from %s.mus.materials.%s.%s_input_code import %s' % (
            self.score_package_name, self.material_name, self.material_name, self.material_name)
        exec(command)
        exec('_material = %s' % self.material_name)
        output_line = '%s = %r' % (self.material_name, _material)
        output_file = file(self.material_output_data, 'w')
        output_file.write(output_line)
        output_file.close()
        print 'Output written to %s_output_data.py.' % self.material_name
