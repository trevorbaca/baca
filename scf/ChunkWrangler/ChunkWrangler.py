from baca.scf.ChunkProxy import ChunkProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class ChunkWrangler(PackageWrangler):

    def __init__(self, session=None):
        import baca
        PackageWrangler.__init__(self, 'baca.sketches', 'mus.chunks', session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'chunks'

    ### PUBLIC METHODS ###

    def create_chunk_interactively(self):
        chunk_proxy = ChunkProxy(session=self.session)
        chunk_proxy.create_chunk_interactively()

    def get_package_proxy(self, package_importable_name):
        return ChunkProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.create_chunk_interactively()
        else:
            chunk_proxy = self.get_package_proxy(result)
            chunk_proxy.run()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.wrangled_package_short_names()
        section = menu.make_new_section()
        section.append(('new', 'new chunk'))
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
