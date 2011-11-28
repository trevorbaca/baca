from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class ChunkWrangler(PackageWrangler, PackageProxy):

    def __init__(self, purview_package_short_name, session=None):
        package_importable_name = '.'.join([purview_package_short_name, 'mus', 'chunks'])
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)

    ### PUBLIC ATTRIBUTES ###

    @property
    def ChunkProxy(self):
        from baca.scf.ChunkProxy import ChunkProxy
        return ChunkProxy

    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def create_chunk_interactively(self):
        chunk_proxy = self.ChunkProxy()
        chunk_proxy.purview = self.purview
        chunk_proxy.create_chunk_interactively()

    def get_package_proxy(self, package_importable_name):
        return self.ChunkProxy(package_importable_name)

    def manage_chunks(self):
        self.print_not_implemented()
