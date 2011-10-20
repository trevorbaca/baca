from baca.scf.PackageProxy import PackageProxy


class ChunkProxy(PackageProxy):

    ### PUBLIC ATTRIBUTES ###

    @property
    def chunk_spaced_name(self):
        return self.package_spaced_name

    @property
    def chunk_underscored_name(self):
        return self.package_short_name

    ### PUBLIC METHODS ###

    def create_chunk(self):
        self.create_directory()
        self.create_initializer()
        self.proceed()

    def create_chunk_interactively(self):
        if self.purview is None:
            self.set_purview_interactively()
        if self.package_spaced_name is None:
            self.set_package_spaced_name_interactively()
        if self.score_template is None:
            self.set_score_template_interactively()
        self.write_to_disk()
        self.proceed()

    # TODO: move to package proxy
    def delete_chunk(self):
        result = self.remove()
        if result:
            self.proceed()

    def set_chunk_spaced_name_interactively(self):
        getter = self.UserInputGetter(client=self.where(), menu_header=menu_header)
        getter.menu_body = 'create chunk'
        getter.prompts.append('chunk name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        chunk_spaced_name = getter.run()
        package_short_name = chunk_spaced_name.replace(' ', '_')
        package_importable_name = '.'.join([self.package_importable_name, package_short_name])
        chunk_proxy = ChunkProxy(package_importable_name)
        chunk_proxy.create_chunk()
        self.proceed()

    def manage_chunk(self, menu_header=None):
        while True:
            menu = self.Menu(client=self.where())
            menu.menu_header = menu_header
            menu.menu_body = self.chunk_spaced_name
            menu.named_pairs.append(('n', 'initializer'))
            menu.secondary_named_pairs.append(('d', 'delete'))
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'd':
                self.delete_chunk()
                break
            elif key == 'n':
                self.edit_initializer()
