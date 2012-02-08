from baca.scf.PackageProxy import PackageProxy
import os


class ScorePackageProxy(PackageProxy):

    def __init__(self, score_package_short_name, session=None):
        import baca
        PackageProxy.__init__(self, score_package_short_name, session=session)
        self._dist_proxy = baca.scf.DistDirectoryProxy(score_package_short_name, session=self.session)
        self._etc_proxy = baca.scf.EtcDirectoryProxy(score_package_short_name, session=self.session)
        self._exg_proxy = baca.scf.ExgDirectoryProxy(score_package_short_name, session=self.session)
        self._mus_proxy = baca.scf.MusPackageProxy(score_package_short_name, session=self.session)
        self._chunk_wrangler = baca.scf.ChunkPackageWrangler(session=self.session)
        self._material_package_wrangler = baca.scf.MaterialPackageWrangler(session=self.session)
        self._material_package_maker_wrangler = baca.scf.MaterialPackageMakerWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def annotated_title(self):
        if isinstance(self.year_of_completion, int):
            return self.title_with_year
        else:
            return self.title

    @property
    def breadcrumb(self):
        return self.annotated_title

    @property
    def chunk_wrangler(self):
        return self._chunk_wrangler

    @property
    def chunks_package_directory_name(self):
        return os.path.join(self.directory_name, 'mus', 'chunks')

    @property
    def chunks_package_importable_name(self):
        return '.'.join([self.package_importable_name, 'mus', 'chunks'])

    @property
    def chunks_package_initializer_file_name(self):
        return os.path.join(self.chunks_package_directory_name, '__init__.py')

    @property
    def composer(self):
        return self.get_tag('composer')

    @property
    def dist_pdf_directory_name(self):
        return os.path.join(self.dist_proxy.directory_name, 'pdf')

    @property
    def dist_proxy(self):
        return self._dist_proxy

    @property
    def etc_proxy(self):
        return self._etc_proxy

    @property
    def exg_proxy(self):
        return self._exg_proxy

    @property
    def has_correct_directory_structure(self):
        return all([os.path.exists(name) for name in self.top_level_directory_names])

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
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler

    @property
    def materials_package_directory_name(self):
        return os.path.join(self.directory_name, 'mus', 'materials')

    @property
    def materials_package_importable_name(self):
        return '.'.join([self.package_importable_name, 'mus', 'materials'])

    @property
    def materials_package_initializer_file_name(self):
        return os.path.join(self.materials_package_directory_name, '__init__.py')

    @property
    def mus_proxy(self):
        return self._mus_proxy

    @property
    def score_initializer_file_names(self):
        return (
            self.initializer_file_name,
            self.mus_proxy.initializer_file_name,
            )

    @property
    def score_package_wranglers(self):
        return (
            self.chunk_wrangler,
            self.material_package_wrangler,
            )

    @property
    def title(self):
        return self.get_tag('title') or self.untitled_indicator

    @property
    def title_with_year(self):
        if self.year_of_completion:
            return '{} ({})'.format(self.title, self.year_of_completion)
        else:
            return self.title

    @property
    def top_level_directory_names(self):
        return tuple([x.directory_name for x in self.top_level_directory_proxies])

    @property
    def top_level_directory_proxies(self):
        return (
            self.dist_proxy,
            self.etc_proxy,
            self.exg_proxy,
            self.mus_proxy,
            )

    @property   
    def untitled_indicator(self):
        return '(untitled score)'
        
    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def forces_tagline():
        def fget(self):
            return self.get_tag('forces_tagline')
        def fset(self, forces_tagline):
            return self.add_tag('forces_tagline', forces_tagline)
        return property(**locals())

    @apply
    def year_of_completion():
        def fget(self):
            return self.get_tag('year_of_completion')
        def fset(self, year_of_completion):
            return self.add_tag('year_of_completion', year_of_completion)
        return property(**locals())

    ### PUBLIC METHODS ###

    def edit_forces_tagline_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('Forces tagline')
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('forces_tagline', result)

    def edit_instrumentation_specifier_interactively(self):
        import baca
        target = self.get_tag('instrumentation')
        editor = baca.scf.editors.InstrumentationEditor(session=self.session, target=target)
        editor.run() # maybe check for backtracking after this?
        self.add_tag('instrumentation', editor.target)

    def edit_title_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('new title')
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('title', result)

    def edit_year_of_completion_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_or_none('year of completion')
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('year_of_completion', result)

    def fix_package_structure(self, is_interactive=True):
        if self.package_short_name == 'recursif':
            return
        for directory_name in self.top_level_directory_names:
            if not os.path.exists(directory_name):
                prompt = 'create {!r}? '.format(directory_name)
                if not is_interactive or self.confirm(prompt):
                    os.mkdir(directory_name)
        if not os.path.exists(self.initializer_file_name):
            prompt = 'create {}? '.format(self.initializer_file_name)
            if not is_interactive or self.confirm(prompt):
                initializer = file(self.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        if not os.path.exists(self.mus_proxy.initializer_file_name):
            prompt = 'create {}? '.format(self.mus_proxy.initializer_file_name)
            if not is_interactive or self.confirm(prompt):
                initializer = file(self.mus_proxy.initializer_file_name, 'w')
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
        if not os.path.exists(self.tags_file_name):
            prompt = 'create {}? '.format(self.tags_file_name)
            if not is_interactive or self.confirm(prompt):
                tags_file = file(self.tags_file_name, 'w')
                tags_file.write('from collections import OrderedDict\n')
                tags_file.write('\n')
                tags_file.write('tags = OrderedDict([])\n')
                tags_file.close()
        if not os.path.exists(self.materials_package_directory_name):
            prompt = 'create {}'.format(self.materials_package_directory_name)
            if not is_interactive or self.confirm(prompt):
                os.mkdir(self.materials_package_directory_name)
        if not os.path.exists(self.materials_package_initializer_file_name):
            file(self.materials_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.chunks_package_directory_name):
            prompt = 'create {}'.format(self.chunks_package_directory_name)
            if not is_interactive or self.confirm(prompt):
                os.mkdir(self.chunks_package_directory_name)
        if not os.path.exists(self.chunks_package_initializer_file_name):
            file(self.chunks_package_initializer_file_name, 'w').write('')
        self.proceed('packaged structure fixed.', prompt=is_interactive)

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'h':
            self.chunk_wrangler.run(head=self.package_short_name)
        elif  result == 'm':
            self.material_package_wrangler.run(head=self.package_short_name)
        elif result == 'ft':
            self.edit_forces_tagline_interactively()
        elif result == 'pf':
            self.edit_instrumentation_specifier_interactively()
        elif result == 'tl':
            self.edit_title_interactively()
        elif result == 'yr':
            self.edit_year_of_completion_interactively()
        elif result == 'fix':
            self.fix_package_structure()
        elif result == 'ls':
            self.print_directory_contents()
        elif result == 'profile':
            self.profile_package_structure()
        elif result == 'removescore':
            self.remove_interactively()
        elif result == 'svn':
            self.manage_svn()
        elif result == 'tags':
            self.manage_tags()
        else:
            raise ValueError

    def handle_svn_menu_result(self, result):
        if result == 'add':
            self.svn_add()
        elif result == 'ci':
            self.svn_ci()
            return True
        elif result == 'st':
            self.svn_st()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section = menu.make_new_section()
        section.append(('h', 'chunks'))
        section.append(('m', 'materials'))
        section = menu.make_new_section()
        section.append(('ft', 'forces tagline'))
        section.append(('pf', 'performers'))
        section.append(('tl', 'title'))
        section.append(('yr', 'year of completion'))
        hidden_section = menu.make_new_section(is_hidden=True)
        hidden_section.append(('fix', 'fix package structure'))
        hidden_section.append(('ls', 'list directory contents'))
        hidden_section.append(('profile', 'profile package structure'))
        hidden_section.append(('removescore', 'remove score package'))
        hidden_section.append(('svn', 'manage repository'))
        hidden_section.append(('tags', 'manage tags'))
        return menu

    def make_package_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def make_score_interactively(self):
        self.print_not_implemented()

    def make_svn_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_keyed=False)
        section.append(('st', 'st'))
        section.append(('add', 'add'))
        section.append(('ci', 'ci'))
        return menu

    def manage_svn(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            self.handle_svn_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def profile_package_structure(self, prompt=True):
        if not os.path.exists(self.directory_name):
            raise OSError('directory {!r} does not exist.'.format(self.directory_name))
        if self.package_short_name == 'recursif':
            return
        lines = []
        for subdirectory_name in self.top_level_directory_names:
            lines.append('{} {}'.format(subdirectory_name.ljust(80), os.path.exists(subdirectory_name)))
        for initializer in self.score_initializer_file_names:
            lines.append('{} {}'.format(initializer.ljust(80), os.path.exists(initializer)))
        lines.append('')
        self.display(lines)
        self.proceed(prompt=prompt)

    def remove_interactively(self):
        line = 'WARNING! Score package {!r} will be completely removed.'.format(self.package_importable_name)
        self.display([line, ''])
        getter = self.make_new_getter(where=self.where())
        getter.append_string("type 'clobberscore' to proceed")
        self.push_backtrack()
        should_clobber = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        if should_clobber == 'clobberscore':
            self.push_backtrack()
            self.remove()
            self.pop_backtrack()
            if self.backtrack():
                return
            self.session.is_backtracking_locally = True
        
    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.pop_breadcrumb() 
                continue
            elif self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.pop_breadcrumb()
                continue
            elif self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def summarize_chunks(self):
        chunks = self.chunk_wrangler.package_underscored_names
        lines = []
        if not chunks:
            lines.append('{}Chunks (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Chunks'.format(self.make_tab(1)))
        for chunk in chunks:
            lines.append('{}{}'.format(self.make_tab(2), chunk))
        lines.append('')
        self.display(lines)

    def summarize_materials(self):
        materials = self.material_package_wrangler.package_spaced_names
        lines = []
        if not materials:
            lines.append('{}Materials (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Materials'.format(self.make_tab(1)))
        if materials:
            lines.append('')
        for i, material in enumerate(materials):
            lines.append('{}({}) {}'.format(self.make_tab(1), i + 1, material))
        self.display(lines)
