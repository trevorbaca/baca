from baca.scf.PackageProxy import PackageProxy


class ChunkProxy(PackageProxy):

    def __init__(self, package_importable_name=None, score_template=None, session=None):
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self.score_template = score_template

    ### PUBLIC ATTRIBUTES ###

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
        self.create_directory()
        self.create_initializer()
        self.proceed()

    def create_chunk_interactively(self):
        if self.purview is None:
            self.set_purview_interactively()
        if self.package_spaced_name is None:
            print 'here!'
            self.set_package_spaced_name_interactively()
        if self.score_template is None:
            self.set_score_template_interactively()
        self.write_package_to_disk()
        self.proceed()

    def set_chunk_spaced_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('chunk name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        chunk_spaced_name = getter.run()
        package_short_name = chunk_spaced_name.replace(' ', '_')
        package_importable_name = '.'.join([self.package_importable_name, package_short_name])
        chunk_proxy = ChunkProxy(package_importable_name)
        chunk_proxy.create_chunk()
        self.proceed()

    def manage_chunk(self):
        while True:
            menu = self.make_new_menu(where=self.where())
            menu_section = self.MenuSection()
            menu_section.named_pairs.append(('n', 'initializer'))
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.named_pairs.append(('d', 'delete'))
            menu.menu_sections.append(menu_section)
            key, value = menu.run()
            if key == 'b':
                return key, None
            elif key == 'd':
                self.delete_package()
                break
            elif key == 'n':
                self.edit_initializer()

    def set_score_template_interactively(self):
        self.print_not_implemented()
