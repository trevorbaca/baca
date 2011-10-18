from baca.scf.PackageProxy import PackageProxy
from baca.scf.menuing import Menu
import inspect


class ChunkWrangler(PackageProxy):

    ### PUBLIC METHODS ###

    def create_chunk(self):
        return self.print_not_implemented()

    def create_chunk_interactively(self, menu_header=None):
        menu = Menu(client=self.where(), menu_header=menu_header)
        menu.menu_body = 'create chunk'
        key, value = menu.display_menu()
