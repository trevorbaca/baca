from baca.scf.ChunkWrangler import ChunkWrangler
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.menuing import Menu
from baca.scf.menuing import MenuSection
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StaticMaterialProxy import StaticMaterialProxy
import os


class ScoreProxy(PackageProxy):

    def __init__(self, package_importable_name):
        PackageProxy.__init__(self, package_importable_name)
        self._chunk_wrangler = ChunkWrangler('.'.join([package_importable_name, 'mus', 'chunks']))
        self._material_wrangler = MaterialWrangler(purview=self)
        self._maker_wrangler = MakerWrangler()

    ### PUBLIC ATTRIBUTES ###

    @property
    def chunk_wrangler(self):
        return self._chunk_wrangler

    @property
    def chunks_directory_name(self):
        return self.chunk_wrangler.directory_name

    @property
    def chunks_initializer(self):
        return self.chunk_wrangler.initializer_file_name

    @property
    def chunks_package_importable_name(self):
        return self.chunk_wrangler.package_importable_name

    @property
    def dist_directory_name(self):
        return os.path.join(self.directory_name, 'dist')

    @property
    def dist_pdf_directory_name(self):
        return os.path.join(self.directory_name, 'dist', 'pdf')

    @property
    def exg_directory_name(self):
        return os.path.join(self.directory_name, 'exg')

    @property
    def etc_directory_name(self):
        return os.path.join(self.directory_name, 'etc')

    @property
    def has_correct_directory_structure(self):
        return all([os.path.exists(name) for name in self.score_subdirectory_names])

    @property
    def has_correct_initializers(self):
        return all([os.path.exists(initializer) for initializer in self.score_initializers])

    @property
    def has_correct_package_structure(self):
        return self.has_correct_directory_structure and self.has_correct_initializers

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler

    @property
    def materials_directory_name(self):
        return os.path.join(self.directory_name, 'mus', 'materials')

    @property
    def materials_initializer(self):
        return os.path.join(self.materials_directory_name, '__init__.py')

    @property
    def materials_package_importable_name(self):
        return '.'.join([self.package_importable_name, 'mus', 'materials'])

    @property
    def mus_directory_name(self):
        return os.path.join(self.directory_name, 'mus')

    @property
    def mus_initializer(self):
        return os.path.join(self.mus_directory_name, '__init__.py')

    @property
    def mus_package_importable_name(self):
        return '.'.join([self.package_importable_name, 'mus'])

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

    @property
    def score_initializers(self):
        return (self.initializer,
            self.mus_initializer,
            self.chunks_initializer,
            self.materials_initializer,)

    @property
    def score_subdirectory_names(self):
        return (self.dist_directory_name,
            self.dist_pdf_directory_name,
            self.etc_directory_name,
            self.exg_directory_name,
            self.mus_directory_name,
            self.materials_directory_name,
            self.chunks_directory_name,)

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

    def create_package_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def fix_package_structure(self, is_interactive=True):
        if self.package_short_name == 'recursif':
            return
        for directory_name in self.score_subdirectory_names:
            if not os.path.exists(directory_name):
                prompt = 'Create %s? ' % directory_name
                if not is_interactive or self.query(prompt):
                    os.mkdir(directory_name)
        for initializer in self.score_initializers:
            if not os.path.exists(initializer):
                prompt = 'Create %s? ' % initializer
                if not is_interactive or self.query(prompt):
                    initializer = file(initializer, 'w')
                    initializer.write('')
                    initializer.close()
        lines = []
        initializer = file(self.mus_initializer, 'r')
        found_materials_import = False
        for line in initializer.readlines():
            lines.append(line)
            if line.startswith('import materials'):
                found_materials_import = True
        initializer.close()
        if not found_materials_import:
            lines.insert(0, 'import materials\n')
            initializer = file(self.mus_initializer, 'w')
            initializer.write(''.join(lines))
            initializer.close()

    def iterate_interactive_material_proxies(self):
        for material_proxy in self.iterate_material_proxies():
            if material_proxy.is_interactive:
                yield material_proxy

    def iterate_material_proxies(self):
        for material_package_importable_name in self.list_material_package_importable_names():
            material_proxy = self.get_material_proxy(material_package_importable_name)
            yield material_proxy

    def iterate_static_material_proxies(self):
        for material_proxy in self.iterate_material_proxies():
            if not material_proxy.is_interactive:
                yield material_proxy

    def list_material_package_importable_names(self):
        material_package_importable_names = []
        for material in self.list_material_underscored_names():
            material_package_importable_name = '%s.%s' % (self.materials_package_importable_name, material)
            material_package_importable_names.append(material_package_importable_name)
        return material_package_importable_names

    def list_underscored_chunk_names(self):
        chunks = os.listdir(self.chunks_directory_name)
        chunks = [x for x in chunks if x[0].isalpha()]
        return chunks

    def list_underscored_chunk_names_with_numbers(self):
        numbered_chunks = []
        for i, chunk in enumerate(self.list_underscored_chunk_names()):
            numbered_chunk = (str(i + 1), chunk)
            numbered_chunks.append(numbered_chunk)
        return numbered_chunks

    def list_material_underscored_names(self):
        try:
            materials = os.listdir(self.materials_directory_name)
        except OSError:
            materials = []
        materials = [x for x in materials if x[0].isalpha()]
        return materials

    def list_material_underscored_names_with_numbers(self):
        numbered_materials = []
        for i, material in enumerate(self.list_material_underscored_names()):
            material = material.replace('%s_' % self.package_short_name, '')
            material = material.replace('_', ' ')
            numbered_material = (str(i + 1), material)
            numbered_materials.append(numbered_material)
        return numbered_materials
            
    def manage_chunks(self):
        self.print_not_implemented()

    def manage_materials(self, material_number=None):
        while True:
            result = self.select_material(material_number=material_number)
            if result == 'b':
                return result
            else:
                result.score_title = self.score_title
                result.manage_material()
            material_number = None

    def manage_score(self, menu_header=None, command_string=None):
        while True:
            menu_specifier = Menu(client=self, menu_header=menu_header)
            menu_specifier.menu_body = self.score_title
            menu_section = MenuSection()
            menu_section.menu_section_title = 'Chunks'
            menu_section.menu_section_entries = self.list_underscored_chunk_names_with_numbers()
            menu_section.sentence_length_items.append(('ch', '[create chunk]'))
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSection()
            menu_section.menu_section_title = 'Materials'
            menu_section.menu_section_entries = self.list_material_underscored_names_with_numbers()
            menu_section.sentence_length_items.append(('ms', 'create material by hand'))
            menu_section.sentence_length_items.append(('mi', 'create material interactively'))
            menu_specifier.menu_sections.append(menu_section)
            menu_specifier.hidden_items.append(('svn', 'work with repository'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'ch':
                self.chunk_wrangler.create_chunk_interactively(menu_header=self.score_title)
            elif key == 'ms':
                self.material_wrangler.create_static_material_package_interactively(menu_header=self.score_title)
            elif key == 'mi':
                self.material_wrangler.create_interactive_material_interactively(menu_header=self.score_title)
            elif key == 'svn':
                self.manage_svn(menu_header=self.score_title)
            else:
                try:
                    material_number = int(key)
                    material_underscored_name = self.material_number_to_material_underscored_name(material_number)
                    package_importable_name = '%s.%s' % (self.materials_package_importable_name, material_underscored_name)
                    material_proxy = self.get_material_proxy(package_importable_name)
                    material_proxy.score_title = self.score_title
                    material_proxy.manage_material(menu_header=menu_specifier.menu_title)
                except (TypeError, ValueError):
                    pass

    def manage_svn(self, menu_header=None):
        while True:
            menu_specifier = Menu(client=self)
            menu_specifier.menu_header = menu_header
            menu_specifier.menu_body = 'repository commands'
            menu_section = MenuSection()
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'add':
                self.svn_add()
            elif key == 'ci':
                self.svn_ci()
                break
            elif key == 'st':
                self.svn_st()

    def material_number_to_material_underscored_name(self, material_number):
        material_index = material_number - 1
        material_underscored_name = self.list_material_underscored_names()[material_index]
        return material_underscored_name

    def profile_package_structure(self):
        if not os.path.exists(self.directory_name):
            raise OSError('directory %r does not exist.' % self.directory_name)
        if self.package_short_name == 'recursif':
            return
        for subdirectory_name in self.score_subdirectory_names:
            print '%s %s' % (subdirectory_name.ljust(80), os.path.exists(subdirectory_name))
        for initializer in self.score_initializers:
            print '%s %s' % (initializer.ljust(80), os.path.exists(initializer))

    def summarize_chunks(self):
        chunks = self.list_underscored_chunk_names()
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
        materials = self.list_material_underscored_names()
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
