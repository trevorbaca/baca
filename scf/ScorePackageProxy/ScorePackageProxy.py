from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.SCFProxyObject import SCFProxyObject
import os


class ScorePackageProxy(SCFProxyObject):

    def __init__(self, score_package_name):
        self.score_package_directory = os.path.join(os.environ.get('SCORES'), score_package_name)
        self.chunks_directory = os.path.join(self.score_package_directory, 'mus', 'chunks')
        self.materials_directory = os.path.join(self.score_package_directory, 'mus', 'materials')
        self.score_package_initializer = os.path.join(self.score_package_directory, '__init__.py')
        self.score_package_name = score_package_name

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.score_package_name)

    ### PRIVATE METHODS ###

    def _get_conditional_user_input(self, is_interactive, prompt = None):
        if not is_interactive:
            return True
        response = raw_input(prompt)
        return response.lower() == 'y'

    def _read_initializer_metadata(self, name):
        initializer = file(self.score_package_initializer, 'r')
        for line in initializer.readlines():
            if line.startswith(name):
                initializer.close()
                executable_line = line.replace(name, 'result')
                exec(executable_line)
                return result

    def _write_initializer_metadata(self, name, value):
        new_lines = []
        initializer = file(self.score_package_initializer, 'r')
        found_existing_line = False
        for line in initializer.readlines():
            if line.startswith(name):
                found_existing_line = True
                new_line = '%s = %r\n' % (name, value)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        if not found_existing_line:
            new_line = '%s = %r\n' % (name, value)
            new_lines.append(new_line)
        initializer.close()
        initializer = file(self.score_package_initializer, 'w')
        initializer.write(''.join(new_lines))
        initializer.close()

    ### PUBLIC ATTRIBUTES ###

    @apply
    def score_composer():
        def fget(self):
            return self._read_initializer_metadata('score_composer')
        def fset(self, score_title):
            return self._write_initializer_metadata('score_composer', score_title)
        return property(**locals())

    @apply
    def score_forces():
        def fget(self):
            return self._read_initializer_metadata('score_forces')
        def fset(self, score_title):
            return self._write_initializer_metadata('score_forces', score_title)
        return property(**locals())

    @apply
    def score_title():
        def fget(self):
            return self._read_initializer_metadata('score_title')
        def fset(self, score_title):
            return self._write_initializer_metadata('score_title', score_title)
        return property(**locals())

    @apply
    def score_year():
        def fget(self):
            return self._read_initializer_metadata('score_year')
        def fset(self, score_title):
            return self._write_initializer_metadata('score_year', score_title)
        return property(**locals())

    ### PUBLIC METHODS ###

    def create_materials_package(self):
        response = raw_input('material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        material_package_name = '%s_%s' % (self.score_package_name, response)
        print 'package name will be %s.\n' % material_package_name
        self.confirm()
        target = os.path.join(self.materials_directory, material_package_name)
        if os.path.exists(target):
            raise OSError('directory %r already exists.' % target)
        os.mkdir(target)
        initializer = file(os.path.join(target, '__init__.py'), 'w')
        initializer.write('from %s_output_data import *\n' % material_package_name)
        initializer.close()
        input_code = '%s_input_code.py' % material_package_name
        input_code = file(os.path.join(target, input_code), 'w')
        input_code.write('')
        input_code.close()
        output_data = '%s_output_data.py' % material_package_name
        output_data = file(os.path.join(target, output_data), 'w')
        output_data.write('')
        output_data.close()
        print '%s created.\n' % material_package_name

    def create_score_package_directory_structure(self):
        self.fix_score_package_directory_structure(is_interactive = False)

    def fix_score_package_directory_structure(self, is_interactive = True):
        if not os.path.exists(self.score_package_directory):
            raise OSError('directory %r does not exist.' % self.score_package_directory)

        if self.score_package_name == 'poeme':
            return

        target = os.path.join(self.score_package_directory, '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/__init__.py? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                initializer = file(target, 'w')
                initializer.write('')
                initializer.close()

        target = os.path.join(self.score_package_directory, 'dist')
        if not os.path.exists(target):
            prompt = 'Create %s/dist/? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'dist', 'pdf')
        if not os.path.exists(target):
            prompt = 'Create %s/dist/pdf/? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'etc')
        if not os.path.exists(target):
            prompt = 'Create %s/etc/? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'exg')
        if not os.path.exists(target):
            prompt = 'Create %s/exg/? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'mus')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'mus', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/__init__.py? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                initializer = file(target, 'w')
                initializer.write('import materials\n')
                initializer.close()

        target = os.path.join(self.score_package_directory, 'mus', 'chunks')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/chunks? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'mus', 'chunks', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/chunks/__init__.py? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                initializer = file(target, 'w')
                initializer.write('')
                initializer.close()

        target = os.path.join(self.score_package_directory, 'mus', 'materials')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/materials? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                os.mkdir(target)

        target = os.path.join(self.score_package_directory, 'mus', 'materials', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/materials/__init__.py? ' % self.score_package_name
            if self._get_conditional_user_input(is_interactive, prompt = prompt):
                initializer = file(target, 'w')
                initializer.write('')
                initializer.close()

    def list_chunks(self):
        chunks = os.listdir(self.chunks_directory)
        chunks = [x for x in chunks if x[0].isalpha()]
        return chunks

    def list_materials(self):
        materials = os.listdir(self.materials_directory)
        materials = [x for x in materials if x[0].isalpha()]
        return materials

    def manage_chunks(self):
        self.print_not_implemented()

    def manage_materials(self):
        while True:
            result = self.select_material()
            if isinstance(result, MaterialPackageProxy):
                result.score_title = self.score_title
                result.manage_material()
            elif result == 'b':
                return result

    def manage_score(self):
        is_first_pass = True
        while True:
            is_redraw = False
            if is_first_pass:
                self.print_menu_title('%s - main menu\n' % self.score_title)
                self.summarize_chunks()
                self.summarize_materials()
            named_pairs = [('h', 'chunks'), ('m', 'materials')]
            kwargs = {'named_pairs': named_pairs, 'indent_level': 1}
            kwargs.update({'is_nearly': False, 'show_options': is_first_pass})
            key, value = self.display_menu(**kwargs)
            result = None
            if key == 'd':
                is_redraw = True
            elif key == 'h':
                self.manage_chunks()
            elif key == 'm':
                result = self.manage_materials()
            elif key == 'q':
                raise SystemExit
            elif key == 'x':
                self.exec_statement()
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False

    def profile_score_package_directory_structure(self):
        if not os.path.exists(self.score_package_directory):
            raise OSError('directory %r does not exist.' % self.score_package_directory)
        if self.score_package_name == 'poeme':
            return
        print '%s/__init__.py                  ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, '__init__.py')))
        print '%s/dist/                          ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'dist')))
        print '%s/dist/pdf                     ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'dist', 'pdf')))
        print '%s/etc/                           ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'etc')))
        print '%s/exg/                           ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'exg')))
        print '%s/mus/                           ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'mus')))
        print '%s/mus/__init__.py            ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', '__init__.py')))
        print '%s/mus/chunks/                  ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'chunks')))
        print '%s/mus/chunks/__init__.py   ' % self.score_package_name,
        print str(os.path.exists(os.path.join(
            self.score_package_directory, 'mus', 'chunks', '__init__.py')))
        print '%s/mus/materials/             ' % self.score_package_name,
        print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'materials')))
        print '%s/mus/materials/__init__.py' % self.score_package_name,
        print str(os.path.exists(os.path.join(
            self.score_package_directory, 'mus', 'materials', '__init__.py')))

    def run_chunk_selection_interface(self):
        raise NotImplementedError

    def select_material(self):
        is_first_pass = True
        while True:
            is_redraw = False
            if is_first_pass:
                self.print_menu_title('%s - materials\n' % self.score_title)
            materials = self.list_materials()
            named_pairs = [('n', 'new')]
            kwargs = {'values_to_number': materials, 'named_pairs': named_pairs}
            kwargs.update({'indent_level': 1, 'show_options': is_first_pass})
            key, material_name = self.display_menu(**kwargs)
            if key == 'b':
                return key
            elif key == 'd':
                is_redraw = True
            elif key == 'n':
                self.create_materials_package()
            elif key == 'q':
                raise SystemExit
            elif key == 'r':
                self.rename_materials_package()
            elif key == 'x':
                self.exec_statement()
            else:
                material_package_proxy = MaterialPackageProxy(self.score_package_name, material_name)
                return material_package_proxy
            if is_redraw:
                is_first_pass = True
            else:
                is_first_pass = False

    def summarize_chunks(self):
        chunks = self.list_chunks()
        print self.tab(1),
        print 'Chunks (%s)' % len(chunks)
        for chunk in chunks:
            print self.tab(2),
            print chunk
        print ''

    def summarize_materials(self):
        materials = self.list_materials()
        print self.tab(1),
        print 'Materials (%s)' % len(materials)
        if materials:
            print ''
        for material in materials:
            print self.tab(1),
            print material
