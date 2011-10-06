from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.MakersProxy import MakersProxy
from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.PackageProxy import PackageProxy
import os


class ScorePackageProxy(PackageProxy, _MaterialPackageMaker):

    def __init__(self, package_name):
        directory = os.path.join(os.environ.get('SCORES'), package_name)
        importable_module_name = package_name
        PackageProxy.__init__(self, directory, importable_module_name)
        self.chunks_directory = os.path.join(self.directory, 'mus', 'chunks')
        self.materials_directory = os.path.join(self.directory, 'mus', 'materials')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.package_name)

    ### PRIVATE METHODS ###

    def _get_conditional_user_input(self, is_interactive, prompt=None):
        if not is_interactive:
            return True
        response = raw_input(prompt)
        return response.lower() == 'y'

    def _read_initializer_metadata(self, name):
        initializer = file(self.initializer, 'r')
        for line in initializer.readlines():
            if line.startswith(name):
                initializer.close()
                executable_line = line.replace(name, 'result')
                exec(executable_line)
                return result

    def _write_initializer_metadata(self, name, value):
        new_lines = []
        initializer = file(self.initializer, 'r')
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
        initializer = file(self.initializer, 'w')
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
            package_prefix = self.package_name)

    def create_score_package_directory_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def fix_score_package_directory_structure(self, is_interactive=True):
        if not os.path.exists(self.directory):
            raise OSError('directory %r does not exist.' % self.directory)

        if self.package_name == 'poeme':
            return

        target = os.path.join(self.directory, '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/__init__.py? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                initializer = file(target, 'w')
                initializer.write('')
                initializer.close()

        target = os.path.join(self.directory, 'dist')
        if not os.path.exists(target):
            prompt = 'Create %s/dist/? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'dist', 'pdf')
        if not os.path.exists(target):
            prompt = 'Create %s/dist/pdf/? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'etc')
        if not os.path.exists(target):
            prompt = 'Create %s/etc/? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'exg')
        if not os.path.exists(target):
            prompt = 'Create %s/exg/? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'mus')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'mus', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/__init__.py? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                initializer = file(target, 'w')
                initializer.write('import materials\n')
                initializer.close()

        target = os.path.join(self.directory, 'mus', 'chunks')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/chunks? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'mus', 'chunks', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/chunks/__init__.py? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                initializer = file(target, 'w')
                initializer.write('')
                initializer.close()

        target = os.path.join(self.directory, 'mus', 'materials')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/materials? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
                os.mkdir(target)

        target = os.path.join(self.directory, 'mus', 'materials', '__init__.py')
        if not os.path.exists(target):
            prompt = 'Create %s/mus/materials/__init__.py? ' % self.package_name
            if self._get_conditional_user_input(is_interactive, prompt=prompt):
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
            material = material.replace('%s_' % self.package_name, '')
            material = material.replace('_', ' ')
            numbered_material = (str(i + 1), material)
            numbered_materials.append(numbered_material)
        return numbered_materials
            
    def manage_chunks(self):
        self.print_not_implemented()

    def manage_materials(self, material_number=None):
        while True:
            result = self.select_material(material_number=material_number)
            if isinstance(result, MaterialPackageProxy):
                result.score_title = self.score_title
                result.manage_material()
            elif result == 'b':
                return result
            material_number = None

    def manage_score(self, menu_header=None, command_string=None):
        from baca.scf.MenuSectionSpecifier import MenuSectionSpecifier
        from baca.scf.MenuSpecifier import MenuSpecifier
        while True:
            menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier.menu_body = self.score_title
            menu_section = MenuSectionSpecifier()
            menu_section.menu_section_title = 'Chunks'
            menu_section.menu_section_entries = self.list_numbered_chunks()
            menu_section.sentence_length_items.append(('ch', '[make new chunk by hand]'))
            menu_section.sentence_length_items.append(('ci', '[make new chunk interactively]'))
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSectionSpecifier()
            menu_section.menu_section_title = 'Materials'
            menu_section.menu_section_entries = self.list_numbered_materials()
            menu_section.sentence_length_items.append(('mh', 'make new material by hand'))
            menu_section.sentence_length_items.append(('mi', 'make new material interactively'))
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSectionSpecifier()
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('cm', 'commit changes'))
            menu_specifier.menu_sections.append(menu_section)
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'ch':
                key, value = self.make_new_chunk_by_hand()
            elif key == 'ci':
                key, value = self.make_new_chunk_interactively()
            elif key == 'cm':
                self.svn_cm()
            elif key == 'h':
                key, value = self.manage_chunks()
            elif key == 'mh':
                key, value = self.make_new_material_by_hand()
            elif key == 'mi':
                key, value = self.make_new_material_interactively()
            elif key == 'st':
                self.svn_st()
            else:
                try:
                    material_number = int(key)
                    material_name = self.material_number_to_material_name(material_number)
                    material_package_proxy = MaterialPackageProxy(self.package_name, material_name)
                    material_package_proxy.score_title = self.score_title
                    material_package_proxy.manage_material(menu_header=menu_specifier.menu_title)
                except (TypeError, ValueError):
                    pass

    def make_new_chunk_by_hand(self):
        return self.print_not_implemented()

    def make_new_chunk_interactively(self):
        return self.print_not_implemented()

    def make_new_material_by_hand(self):
        return self.create_materials_package()

    def make_new_material_interactively(self):
        while True:
            makers_proxy = MakersProxy()
            key, value = makers_proxy.select_interactive_maker(score_title=self.score_title)
            if value is None:
                break
            else:
                maker = value
            maker.score_title = self.score_title
            maker.materials_directory = self.materials_directory
            result = maker.edit_interactively()
            if result:
                break
        return True, None

    def material_number_to_material_name(self, material_number):
        material_index = material_number - 1
        material_name = self.list_materials()[material_index]
        return material_name

    def profile_score_package_directory_structure(self):
        if not os.path.exists(self.directory):
            raise OSError('directory %r does not exist.' % self.directory)
        if self.package_name == 'poeme':
            return
        print '%s/__init__.py                  ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, '__init__.py')))
        print '%s/dist/                          ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'dist')))
        print '%s/dist/pdf                     ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'dist', 'pdf')))
        print '%s/etc/                           ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'etc')))
        print '%s/exg/                           ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'exg')))
        print '%s/mus/                           ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus')))
        print '%s/mus/__init__.py            ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus', '__init__.py')))
        print '%s/mus/chunks/                  ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus', 'chunks')))
        print '%s/mus/chunks/__init__.py   ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus', 'chunks', '__init__.py')))
        print '%s/mus/materials/             ' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus', 'materials')))
        print '%s/mus/materials/__init__.py' % self.package_name,
        print str(os.path.exists(os.path.join(self.directory, 'mus', 'materials', '__init__.py')))

    def run_chunk_selection_interface(self):
        self.print_not_implemented()

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
