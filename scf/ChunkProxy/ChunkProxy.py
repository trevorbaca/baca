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

    # TODO: move to package proxy
    def delete_chunk(self):
        result = self.remove()
        if result:
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
