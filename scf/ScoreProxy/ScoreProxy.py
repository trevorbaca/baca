from baca.scf.PackageProxy import PackageProxy
import os


class ScoreProxy(PackageProxy):

    def __init__(self, score_package_short_name, session=None):
        import baca
        PackageProxy.__init__(self, score_package_short_name, session=session)
        self._dist_proxy = baca.scf.DistProxy(score_package_short_name, session=session)
        self._etc_proxy = baca.scf.EtcProxy(score_package_short_name, session=session)
        self._exg_proxy = baca.scf.ExgProxy(score_package_short_name, session=session)
        self._mus_proxy = baca.scf.MusProxy(score_package_short_name, session=session)
        self._chunk_wrangler = baca.scf.ChunkWrangler(score_package_short_name, session=session)
        self._material_wrangler = baca.scf.MaterialWrangler(score_package_short_name, session=session)
        self._maker_wrangler = baca.scf.MakerWrangler(session=session)

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
        return all([os.path.exists(initializer) for initializer in self.score_initializer_file_names])

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
    def score_initializer_file_names(self):
        return (self.initializer_file_name,
            self.mus_proxy.initializer_file_name,
            self.chunk_wrangler.initializer_file_name,
            self.material_wrangler.initializer_file_name,)

    @property
    def score_package_wranglers(self):
        return (self.chunk_wrangler,
            self.material_wrangler,)

    @property
    def title(self):
        return self.get_tag('title')

    @property
    def title_with_year(self):
        if self.year_of_completion:
            return '{} ({})'.format(self.title, self.year_of_completion)
        else:
            return self.title

    @property
    def top_level_subdirectories(self):
        return (self.dist_proxy,
            self.etc_proxy,
            self.exg_proxy,
            self.mus_proxy,)
        
    @apply
    def year_of_completion():
        def fget(self):
            return self.get_tag('year_of_completion')
        def fset(self, year_of_completion):
            return self.add_tag('year_of_completion', year_of_completion)
        return property(**locals())

    ### PUBLIC METHODS ###

    def create_package_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def edit_instrumentation_specifier_interactively(self):
        import baca
        target = self.get_tag('instrumentation')
        editor = baca.scf.editors.InstrumentationSpecifierEditor(session=self.session, target=target)
        target = editor.edit_interactively()
        self.add_tag('instrumentation', target)

    def fix_package_structure(self, is_interactive=True):
        if self.package_short_name == 'recursif':
            return
        for directory_name in self.score_subdirectory_names:
            if not os.path.exists(directory_name):
                prompt = 'Create {}? '.format(directory_name)
                if not is_interactive or self.query(prompt):
                    os.mkdir(directory_name)
        for initializer in self.score_initializer_file_names:
            if not os.path.exists(initializer):
                prompt = 'Create {}? '.format(initializer)
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

    def handle_main_menu_response(self, key, value):
        result = False
        if key is None:
            pass
        elif key == 'b':
            result = True
        elif key == 'ch':
            self.chunk_wrangler.create_chunk_interactively()
        elif key == 'instr':
            self.edit_instrumentation_specifier_interactively()
        elif key == 'mi':
            self.material_wrangler.create_interactive_material_interactively()
        elif key == 'ms':
            self.material_wrangler.create_static_material_package_interactively()
        elif key == 'svn':
            return self.manage_svn()
        elif key == 'tags':
            return self.manage_tags()
        elif key.startswith('h'):
            chunk_spaced_name = value
            chunk_underscored_name = chunk_spaced_name.replace(' ', '_')
            package_importable_name = '{}.{}'.format(
                self.chunk_wrangler.package_importable_name, chunk_underscored_name)
            chunk_proxy = self.chunk_wrangler.ChunkProxy(package_importable_name)
            chunk_proxy.title = self.title
            result = chunk_proxy.manage_chunk()
        elif key.startswith('m'):
            material_underscored_name = value
            package_importable_name = '{}.{}'.format(
                self.material_wrangler.package_importable_name, material_underscored_name)
            material_proxy = self.material_wrangler.get_package_proxy(package_importable_name)
            result = material_proxy.manage_material()
        if result:
            return True
        else:
            return False

    def handle_svn_response(self, key, value):
        if key == 'b':
            return True
        elif key == 'add':
            self.svn_add()
        elif key == 'ci':
            self.svn_ci()
            return True
        elif key == 'st':
            self.svn_st()

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'Chunks'
        menu_section.items_to_number = self.chunk_wrangler.iterate_package_spaced_names()
        menu_section.entry_prefix = 'h'
        menu_section.sentence_length_items.append(('ch', '[create chunk]'))
        menu.menu_sections.append(menu_section)
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'Materials'
        menu_section.items_to_number = self.material_wrangler.iterate_package_underscored_names()
        menu_section.entry_prefix = 'm'
        menu_section.sentence_length_items.append(('mi', 'create interactive material'))
        menu_section.sentence_length_items.append(('ms', 'create static material'))
        menu.menu_sections.append(menu_section)
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'Setup'
        menu_section.sentence_length_items.append(('instr', 'edit instrumentation'))
        menu.menu_sections.append(menu_section)
        menu.hidden_items.append(('svn', 'work with repository'))
        menu.hidden_items.append(('tags', 'work with tags'))
        return menu

    def make_svn_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu_section.sentence_length_items.append(('st', 'svn status'))
        menu_section.sentence_length_items.append(('add', 'svn add'))
        menu_section.sentence_length_items.append(('ci', 'svn commit'))
        menu.menu_sections.append(menu_section)
        return menu

    def manage_score(self):
        self.session.menu_pieces.append(self.title)
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            print 'foo', key, value
            if self.session.session_is_complete:
                return True
            if self.handle_main_menu_response(key, value):
                break
        self.session.menu_pieces.pop()

    def manage_svn(self):
        self.session.menu_pieces.append('repository commands')
        while True:
            menu = self.make_svn_menu()
            key, value = menu.run()
            if self.session.session_is_complete:
                return True
            if self.handle_svn_response(key, value):
                break
        self.session.menu_pieces.pop()

    def profile_package_structure(self):
        if not os.path.exists(self.directory_name):
            raise OSError('directory {!r} does not exist.'.format(self.directory_name))
        if self.package_short_name == 'recursif':
            return
        lines = []
        for subdirectory_name in self.score_subdirectory_names:
            lines.append('{} {}'.format(subdirectory_name.ljust(80), os.path.exists(subdirectory_name)))
        for initializer in self.score_initializer_file_names:
            lines.append('{} {}'.format(initializer.ljust(80), os.path.exists(initializer)))
        self.display_lines(lines)

    def run_score_package_creation_wizard(self):
        self.print_not_implemented()

    def summarize_chunks(self):
        chunks = list(self.chunk_wrangler.iterate_package_underscored_names())
        lines = []
        if not chunks:
            lines.append('{}Chunks (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Chunks'.format(self.make_tab(1)))
        for chunk in chunks:
            lines.append('{}{}'.format(self.make_tab(2), chunk))
        lines.append('')
        self.display_lines(lines)

    def summarize_materials(self):
        materials = list(self.material_wrangler.iterate_package_underscored_names())
        lines = []
        if not materials:
            lines.append('{}Materials (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Materials'.format(self.make_tab(1)))
        if materials:
            lines.append('')
        for i, material in enumerate(materials):
            lines.append('{}({}) {}'.format(self.make_tab(1), i + 1, material.replace('_', ' ')))
        self.display_lines(lines)
