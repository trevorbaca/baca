from baca.scf.ChunkPackageProxy import ChunkPackageProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class ChunkPackageProxyWrangler(PackageWrangler):

    def __init__(self, session=None):
        import baca
        PackageWrangler.__init__(self, self.sketches_package_importable_name, 'mus.chunks', session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'chunks'

    ### PUBLIC METHODS ###

    def make_chunk_interactively(self):
        chunk_proxy = ChunkPackageProxy(session=self.session)
        chunk_proxy.make_chunk_interactively()

    def get_package_proxy(self, package_importable_name):
        return ChunkPackageProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_chunk_interactively()
        else:
            chunk_proxy = self.get_package_proxy(result)
            chunk_proxy.run()

    def make_main_menu(self, head=None):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_wrangled_package_short_names(head=head)
        section = menu.make_new_section()
        section.append(('new', 'new chunk'))
        return menu

    def run(self, user_input=None, clear=True, head=None, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
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
        self.restore_breadcrumbs(cache=cache)
