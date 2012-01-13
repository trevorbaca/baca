from baca.scf.PackageProxy import PackageProxy


class ChunkProxy(PackageProxy):

    def __init__(self, package_importable_name=None, score_template=None, session=None):
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self.score_template = score_template

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
    @property
    def breadcrumb(self):
        return self.chunk_name

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            from abjad.tools import scoretools
            assert isinstance(score_template, (scoretools.Score, type(None)))
            self._score_template = score_template
        return property(**locals())

    ### PUBLIC METHODS ###

    def create_chunk(self):
        self.print_not_implemented()

    def create_chunk_interactively(self):
        self.print_not_implemented()
        return
        if self.purview is None:
            self.set_purview_interactively()
        if self.package_spaced_name is None:
            self.set_package_spaced_name_interactively()
        if self.score_template is None:
            self.set_score_template_interactively()
        # TODO: create directory and do other stuff here
        line = 'chunk created.'
        self.proceed(lines=[line])

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.delete_package()
            return False
        elif result == 'n':
            self.edit_initializer()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.append(('n', 'initializer'))
        section = menu.make_new_section()
        section.append(('d', 'delete'))
        return menu

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run()
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()

    def set_chunk_spaced_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        # TODO: implement getter.append_space_delimited_lowercase_string
        getter.prompts.append('chunk name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        result = getter.run()
        if self.backtrack():
            return
        package_short_name = result.replace(' ', '_')
        package_importable_name = '.'.join([self.package_importable_name, package_short_name])
        chunk_proxy = ChunkProxy(package_importable_name)
        chunk_proxy.create_chunk()
        line = 'chunk spaced name set.'
        self.proceed(lines=[line])

    def set_score_template_interactively(self):
        self.print_not_implemented()
