from baca.scf.PackageWrangler import PackageWrangler
import os


# TODO: make also inherit from package proxy 
class ChunkWrangler(PackageWrangler):

    def __init__(self, purview_package_short_name):
        self.package_importable_name = '.'.join([purview_package_short_name, 'mus', 'chunks'])
        directory_name = self.package_importable_name_to_directory_name(self.package_importable_name)
        PackageWrangler.__init__(self, directory_name=directory_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def ChunkProxy(self):
        from baca.scf.ChunkProxy import ChunkProxy
        return ChunkProxy

    # TODO: remove once class inherits from package proxy
    @property
    def initializer_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, '__init__.py')
    
    ### PUBLIC METHODS ###

    def create_chunk_interactively(self, menu_header=None):
        chunk_proxy = self.ChunkProxy()
        chunk_proxy.purview = self.purview
        if self.score is not None:
            menu_header = self.score.title
        else:
            menu_header = None
        chunk_proxy.create_chunk_interactively(menu_header=menu_header)

    def get_package_proxy(self, package_importable_name):
        return self.ChunkProxy(package_importable_name)

    # TODO: implement me
    def manage_chunks(self):
        self.print_not_implemented()
