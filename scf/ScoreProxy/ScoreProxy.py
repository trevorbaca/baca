from baca.scf.PackageProxy import PackageProxy
import os


class ScoreProxy(PackageProxy):

    def __init__(self, score_package_short_name):
        import baca
        PackageProxy.__init__(self, score_package_short_name)
        self._dist_proxy = baca.scf.DistProxy(score_package_short_name)
        self._etc_proxy = baca.scf.EtcProxy(score_package_short_name)
        self._exg_proxy = baca.scf.ExgProxy(score_package_short_name)
        self._mus_proxy = baca.scf.MusProxy(score_package_short_name)
        self._chunk_wrangler = baca.scf.ChunkWrangler(score_package_short_name)
        self._material_wrangler = baca.scf.MaterialWrangler(score_package_short_name)
        self._maker_wrangler = baca.scf.MakerWrangler()

    ### PUBLIC ATTRIBUTES ###

    @property
    def chunk_wrangler(self):
        return self._chunk_wrangler

    @property
    def composer(self):
        return self.get_tag('composer')

    @property
    def dist_proxy(self):
        return self._dist_proxy

    @property
    def dist_pdf_directory_name(self):
        return os.path.join(self.dist_proxy.directory_name, 'pdf')

    @property
    def etc_proxy(self):
        return self._etc_proxy

    @property
    def exg_proxy(self):
        return self._exg_proxy

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
    def instrumentation(self):
        return self.get_tag('instrumentation')

    @property
    def is_score_local_purview(self):
        return True

    @property
    def is_studio_global_purview(self):
        return False

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler

    @property
    def mus_proxy(self):
        return self._mus_proxy

    @property
    def score_initializers(self):
        return (self.initializer_file_name,
            self.mus_proxy.initializer_file_name,
            self.chunk_wrangler.initializer_file_name,
            self.material_wrangler.initializer_file_name,)

    @property
    def score_package_wranglers(self):
        return (self.mus,
            self.chunk_wrangler,
            self.material_wrangler,)

    @property
    def score_subdirectory_names(self):
        return (self.dist_proxy.directory_name,
            self.dist_pdf_directory_name,
            self.etc_proxy.directory_name,
            self.exg_proxy.directory_name,
            self.mus_proxy.directory_name,
            self.material_wrangler.directory_name,
            self.chunk_wrangler.directory_name,)

    @property
    def score_top_level_subdirectories(self):
        return (self.dist_proxy,
            self.etc_proxy,
            self.exg_proxy,
            self.mus_proxy,)
        
    @property
    def title(self):
        return self.get_tag('title')

    @property
    def year_of_completion(self):
        return self.get_tag('year_of_completion')

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
        initializer = file(self.mus_proxy.initializer_file_name, 'r')
        found_materials_import = False
        for line in initializer.readlines():
            lines.append(line)
            if line.startswith('import materials'):
                found_materials_import = True
        initializer.close()
        if not found_materials_import:
            lines.insert(0, 'import materials\n')
            initializer = file(self.mus_proxy.initializer_file_name, 'w')
            initializer.write(''.join(lines))
            initializer.close()

    # TODO: use material wrangler instead
    def iterate_interactive_material_proxies(self):
        for material_proxy in self.iterate_material_proxies():
            if material_proxy.is_interactive:
                yield material_proxy

    # TODO: use material proxy instead
    def iterate_material_proxies(self):
        for material_package_importable_name in self.list_material_package_importable_names():
            material_proxy = self.material_wrangler.get_material_proxy(material_package_importable_name)
            yield material_proxy

    # TODO: use material proxy instead
    def iterate_static_material_proxies(self):
        for material_proxy in self.iterate_material_proxies():
            if not material_proxy.is_interactive:
                yield material_proxy

    def list_chunk_spaced_names_with_numbers(self):
        numbered_chunks = []
        for i, chunk in enumerate(self.chunk_wrangler.list_package_spaced_names()):
            numbered_chunk = (str(i + 1), chunk)
            numbered_chunks.append(numbered_chunk)
        return numbered_chunks

    # TODO: use material wrangler instead
    def list_material_package_importable_names(self):
        material_package_importable_names = []
        for material in self.list_material_underscored_names():
            material_package_importable_name = '%s.%s' % (self.material_wrangler.package_importable_name, material)
            material_package_importable_names.append(material_package_importable_name)
        return material_package_importable_names

    # TODO: use material wrangler instead
    def list_material_underscored_names(self):
        try:
            materials = os.listdir(self.materials_directory_name)
        except OSError:
            materials = []
        materials = [x for x in materials if x[0].isalpha()]
        return materials

    # TODO: use material wrangler instead
    def list_material_underscored_names_with_numbers(self):
        numbered_materials = []
        for i, material in enumerate(self.list_material_underscored_names()):
            material = material.replace('%s_' % self.package_short_name, '')
            material = material.replace('_', ' ')
            numbered_material = (str(i + 1), material)
            numbered_materials.append(numbered_material)
        return numbered_materials
            
    def manage_score(self, menu_header=None, command_string=None):
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = self.score_title
            menu_section = self.MenuSection()
            menu_section.menu_section_title = 'Chunks'
            menu_section.menu_section_entries = self.list_chunk_spaced_names_with_numbers()
            menu_section.menu_section_entry_prefix = 'h'
            menu_section.sentence_length_items.append(('ch', '[create chunk]'))
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.menu_section_title = 'Materials'
            menu_section.menu_section_entries = self.list_material_underscored_names_with_numbers()
            menu_section.menu_section_entry_prefix = 'm'
            menu_section.sentence_length_items.append(('mi', 'create interactive material'))
            menu_section.sentence_length_items.append(('ms', 'create static material'))
            menu.menu_sections.append(menu_section)
            menu.hidden_items.append(('svn', 'work with repository'))
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'ch':
                self.chunk_wrangler.create_chunk_interactively(menu_header=self.score_title)
            elif key == 'mi':
                self.material_wrangler.create_interactive_material_interactively(menu_header=self.score_title)
            elif key == 'ms':
                self.material_wrangler.create_static_material_package_interactively(menu_header=self.score_title)
            elif key == 'svn':
                self.manage_svn(menu_header=self.score_title)
            elif key.startswith('h'):
                chunk_spaced_name = value
                chunk_underscored_name = chunk_spaced_name.replace(' ', '_')
                package_importable_name = '%s.%s' % (self.chunk_wrangler.package_importable_name, chunk_underscored_name)
                chunk_proxy = self.chunk_wrangler.ChunkProxy(package_importable_name)
                chunk_proxy.score_title = self.score_title
                chunk_proxy.manage_chunk(menu_header=menu.menu_title)
            elif key.startswith('m'):
                material_number = key[1:]
                material_number = int(material_number)
                material_underscored_name = self.material_number_to_material_underscored_name(material_number)
                package_importable_name = '%s.%s' % (self.material_wrangler.package_importable_name, material_underscored_name)
                material_proxy = self.material_wrangler.get_material_proxy(package_importable_name)
                material_proxy.score_title = self.score_title
                material_proxy.manage_material(menu_header=menu.menu_title)

    def manage_svn(self, menu_header=None):
        while True:
            menu = self.Menu(client=self.where())
            menu.menu_header = menu_header
            menu.menu_body = 'repository commands'
            menu_section = self.MenuSection()
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.layout = 'line'
            menu.menu_sections.append(menu_section)
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'add':
                self.svn_add()
            elif key == 'ci':
                self.svn_ci()
                break
            elif key == 'st':
                self.svn_st()

    # TODO: use material wrangler instead
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
        chunks = self.chunk_wrangler.list_package_underscored_names()
        print self.tab(1),
        if not chunks:
            print 'Chunks (none yet)'
        else:
            print 'Chunks'
        for chunk in chunks:
            print self.tab(2),
            print chunk
        print ''

    # TODO: use material wrangler instead
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
