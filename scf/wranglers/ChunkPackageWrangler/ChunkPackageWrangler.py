from baca.scf.proxies.ChunkPackageProxy import ChunkPackageProxy
from baca.scf.wranglers.PackageWrangler import PackageWrangler
import os


class ChunkPackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, 
            toplevel_wrangler_target_package_importable_name=self.sketches_package_importable_name, 
            score_resident_wrangled_package_importable_name_infix=\
                self.score_chunks_package_importable_name_infix,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'chunks'

    ### PUBLIC METHODS ###

    def get_package_proxy(self, package_importable_name):
        return ChunkPackageProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_package_interactively()
        else:
            chunk_package_proxy = self.get_package_proxy(result)
            chunk_package_proxy.run()

    def make_package_interactively(self):
        chunk_package_proxy = ChunkPackageProxy(session=self.session)
        chunk_package_proxy.make_package_interactively()

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_wrangled_package_short_names(head=head)
        section = menu.make_section()
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
