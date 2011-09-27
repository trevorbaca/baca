from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.MenuSectionSpecifier import MenuSectionSpecifier
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.SCFProxyObject import SCFProxyObject
import os


class ScorePackageProxy(SCFProxyObject, _MaterialPackageMaker):

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
        return self._create_materials_package(self.materials_directory,
            package_prefix = self.score_package_name)

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

    def list_numbered_chunks(self):
        numbered_chunks = []
        for i, chunk in enumerate(self.list_chunks()):
            numbered_chunk = (str(i + 1), chunk)
            numbered_chunks.append(numbered_chunk)
        return numbered_chunks

    def list_numbered_materials(self):
        numbered_materials = []
        for i, material in enumerate(self.list_materials()):
            material = material.replace('%s_' % self.score_package_name, '')
            material = material.replace('_', ' ')
            numbered_material = (str(i + 1), material)
            numbered_materials.append(numbered_material)
        return numbered_materials
            
    def manage_chunks(self):
        self.print_not_implemented()

    def manage_materials(self, material_number = None):
        while True:
            result = self.select_material(material_number = material_number)
            if isinstance(result, MaterialPackageProxy):
                result.score_title = self.score_title
                result.manage_material()
            elif result == 'b':
                return result
            material_number = None

    def manage_score(self, command_string=None):
        is_first_pass = True
        while True:
            is_redraw = False
            if command_string is None:
                menu_specifier = MenuSpecifier()
                menu_specifier.menu_title = '%s - main menu' % self.score_title
                menu_section = MenuSectionSpecifier()
                menu_section.menu_section_title = 'Chunks'
                menu_section.menu_section_entries = self.list_numbered_chunks()
                menu_specifier.menu_sections.append(menu_section)
                menu_section = MenuSectionSpecifier()
                menu_section.menu_section_title = 'Materials'
                menu_section.menu_section_entries = self.list_numbered_materials()
                menu_specifier.menu_sections.append(menu_section)
                sentence_length_items = [
                    ('h', 'chunks'), 
                    ('m', 'materials'),
                    ]
                menu_specifier.sentence_length_items = sentence_length_items
                command_string, menu_value = menu_specifier.display_menu()
            key = command_string[0]
            result = None
            if key == 'b':
                #break 
                return 'b'
            elif key == 'h':
                self.manage_chunks()
            elif key == 'm':
                if command_string[1:]:
                    material_number = int(command_string[1:])
                else:
                    material_number = None
                result = self.manage_materials(material_number = material_number)
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                is_redraw = True
            elif key == 'x':
                self.exec_statement()
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False
            command_string = None

    def material_number_to_material_name(self, material_number):
        material_index = material_number - 1
        material_name = self.list_materials()[material_index]
        return material_name

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

    def select_material(self, material_number = None):
        if material_number is not None:
            material_name = self.material_number_to_material_name(material_number)
            material_package_proxy = MaterialPackageProxy(self.score_package_name, material_name)
            return material_package_proxy
        is_first_pass = True
        while True:
            is_redraw = False
            if is_first_pass:
                self.print_menu_title('%s - materials\n' % self.score_title)
            materials = self.list_materials()
            materials = [x.replace('_', ' ') for x in materials]
            materials = [x[len(self.score_package_name)+1:] for x in materials]
            named_pairs = [('n', 'new')]
            kwargs = {'values_to_number': materials, 'named_pairs': named_pairs}
            kwargs.update({'indent_level': 1, 'show_options': is_first_pass})
            key, material_name = self.display_menu(**kwargs)
            material_name = '%s_%s' % (self.score_package_name, material_name)
            if key == 'b':
                return key
            elif key == 'n':
                self.create_materials_package()
                is_redraw = True
            elif key == 'q':
                raise SystemExit
            elif key == 'r':
                self.rename_materials_package()
            elif key == 'w':
                is_redraw = True
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
        if not chunks:
            print 'Chunks (none yet)'
        else:
            print 'Chunks'
        for chunk in chunks:
            print self.tab(2),
            print chunk
        print ''

    def summarize_materials(self):
        materials = self.list_materials()
        print self.tab(1),
        if not materials:
            print 'Materials (none yet)'
        else:
            print 'Materials'
        if materials:
            print ''
        for i, material in enumerate(materials):
            print self.tab(1),
            print '(%s) %s' % (i + 1, material.replace('_', ' '))
