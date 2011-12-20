from baca.scf.PackageProxy import PackageProxy
import os


class ScoreProxy(PackageProxy):

    def __init__(self, score_package_short_name, session=None):
        import baca
        PackageProxy.__init__(self, score_package_short_name, session=session)
        self._dist_proxy = baca.scf.DistProxy(score_package_short_name, session=self.session)
        self._etc_proxy = baca.scf.EtcProxy(score_package_short_name, session=self.session)
        self._exg_proxy = baca.scf.ExgProxy(score_package_short_name, session=self.session)
        self._mus_proxy = baca.scf.MusProxy(score_package_short_name, session=self.session)
        self._chunk_wrangler = baca.scf.ChunkWrangler(score_package_short_name, session=self.session)
        self._material_wrangler = baca.scf.MaterialWrangler(score_package_short_name, session=self.session)
        self._maker_wrangler = baca.scf.MakerWrangler(session=self.session)

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

    @apply
    def forces_tagline():
        def fget(self):
            return self.get_tag('forces_tagline')
        def fset(self, forces_tagline):
            return self.add_tag('forces_tagline', forces_tagline)
        return property(**locals())

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

    def edit_forces_tagline_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('Forces tagline')
        result = getter.run()
        if self.session.backtrack():
            return
        self.add_tag('forces_tagline', result)
        return True

    def edit_instrumentation_specifier_interactively(self):
        import baca
        target = self.get_tag('instrumentation')
        editor = baca.scf.editors.InstrumentationEditor(session=self.session, target=target)
        result = editor.run()
        self.add_tag('instrumentation', editor.target)
        return result

    def edit_title_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('new title')
        result = getter.run()
        if self.session.backtrack():
            return
        self.add_tag('title', result)
        return True

    def edit_year_of_completion_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_or_none('year of completion')
        result = getter.run()
        if self.session.backtrack():
            return
        self.add_tag('year_of_completion', result)
        return True

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
        if key == 'ch':
            self.chunk_wrangler.create_chunk_interactively()
        elif key == 'ft':
            self.edit_forces_tagline_interactively()
        elif key == 'mi':
            self.material_wrangler.create_interactive_material_interactively()
        elif key == 'ms':
            self.material_wrangler.create_static_material_package_interactively()
        elif key == 'perf':
            self.edit_instrumentation_specifier_interactively()
        elif key == 'svn':
            self.manage_svn()
        elif key == 'tags':
            self.manage_tags()
        elif key == 'tl':
            self.edit_title_interactively()
        elif key == 'yr':
            self.edit_year_of_completion_interactively()
        elif key.startswith('h'):
            chunk_spaced_name = value
            chunk_underscored_name = chunk_spaced_name.replace(' ', '_')
            package_importable_name = '{}.{}'.format(
                self.chunk_wrangler.package_importable_name, chunk_underscored_name)
            chunk_proxy = self.chunk_wrangler.ChunkProxy(package_importable_name)
            chunk_proxy.title = self.title
            chunk_proxy.run()
        elif key.startswith('m'):
            material_underscored_name = value
            package_importable_name = '{}.{}'.format(
                self.material_wrangler.package_importable_name, material_underscored_name)
            material_proxy = self.material_wrangler.get_package_proxy(package_importable_name)
            material_proxy.run()
        else:
            raise ValueError

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
        menu, section = self.make_new_menu(where=self.where())
        section.section_title = 'chunks'
        section.items_to_number = self.chunk_wrangler.iterate_package_spaced_names()
        section.entry_prefix = 'h'
        section.sentence_length_items.append(('ch', '[create chunk]'))
        section = menu.make_new_section()
        section.section_title = 'materials'
        section.items_to_number = self.material_wrangler.iterate_package_underscored_names()
        section.entry_prefix = 'm'
        section.sentence_length_items.append(('mi', 'create interactive material'))
        section.sentence_length_items.append(('ms', 'create static material'))
        section = menu.make_new_section()
        section.section_title = 'setup'
        section.sentence_length_items.append(('ft', 'forces tagline'))
        section.sentence_length_items.append(('perf', 'performers'))
        section.sentence_length_items.append(('tl', 'title'))
        section.sentence_length_items.append(('yr', 'year of completion'))
        menu.hidden_items.append(('svn', 'work with repository'))
        menu.hidden_items.append(('tags', 'work with tags'))
        return menu

    def make_svn_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.sentence_length_items.append(('st', 'svn status'))
        section.sentence_length_items.append(('add', 'svn add'))
        section.sentence_length_items.append(('ci', 'svn commit'))
        return menu

    def run(self, user_input=None):
        if user_input is not None:
            self.session.user_input = user_input
#        if isinstance(self.year_of_completion, int):
#            self.breadcrumbs.append(self.title_with_year)
#        else:
#            self.breadcrumbs.append(self.title)
        while True:
            # TODO: encapsulate these four lines into public property
            if isinstance(self.year_of_completion, int):
                self.breadcrumbs.append(self.title_with_year)
            else:
                self.breadcrumbs.append(self.title)
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.breadcrumbs.pop() 
                continue
            elif self.session.backtrack():
                break
            elif key is None:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_response(key, value)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.breadcrumbs.pop()
                continue
            elif self.session.backtrack():
                break
            self.breadcrumbs.pop()
        self.breadcrumbs.pop()

    def manage_svn(self):
        self.breadcrumbs.append('repository commands')
        while True:
            menu = self.make_svn_menu()
            key, value = menu.run()
            if self.session.backtrack():
                break
            self.handle_svn_response(key, value)
            if self.session.backtrack():
                break
        self.breadcrumbs.pop()

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
