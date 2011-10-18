from abjad.tools import iotools
from baca.scf.ChunkProxy import ChunkProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.menuing import Menu
from baca.scf.menuing import UserInputGetter
import inspect


class ChunkWrangler(PackageProxy):

    def __init__(self, package_importable_name, purview=None):
        from baca.scf.StudioInterface import StudioInterface
        PackageProxy.__init__(self, package_importable_name)
        self._purview = purview
        if purview is None:
            self._purview = StudioInterface()
        else:
            self._purview = purview

    ### PUBLIC ATTRIBUTES ###

    def purview(self):
        return self._purview

    ### PUBLIC METHODS ###

    def create_chunk_interactively(self, menu_header=None):
        while True:
            menu = UserInputGetter(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'create chunk'
            menu.prompts.append('chunk name> ')
            chunk_name = menu.get_user_input()[0]
            if iotools.is_space_delimited_lowercase_string(chunk_name):
                break
            else:
                print 'Chunk name must be space-delimited lowercase string.'
        package_short_name = chunk_name.replace(' ', '_')
        package_importable_name = '.'.join([self.package_importable_name, package_short_name])
        chunk_proxy = ChunkProxy(package_importable_name)
        chunk_proxy.create_chunk()
        self.proceed()
