from baca.scf.PackageWrangler import PackageWrangler
import os


class ChunkWrangler(PackageWrangler):

    def __init__(self, purview_package_short_name):
        PackageWrangler.__init__(self, '%s.mus.chunks' % purview_package_short_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def ChunkProxy(self):
        from baca.scf.ChunkProxy import ChunkProxy
        return ChunkProxy
    
    ### PUBLIC METHODS ###

    def create_chunk_interactively(self, menu_header=None):
        chunk_proxy = self.ChunkProxy()
        chunk_proxy.purview = self.purview
        if self.score is not None:
            menu_header = self.score.score_title
        else:
            menu_header = None
        chunk_proxy.create_chunk_interactively(menu_header=menu_header)

    def get_package_proxy(self, package_importable_name):
        return self.ChunkProxy(package_importable_name)

    # TODO: implement me
    def manage_chunks(self):
        self.print_not_implemented()
