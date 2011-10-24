from baca.scf.PackageProxy import PackageProxy
import os


class ChunkWrangler(PackageProxy):

    def __init__(self, purview_package_short_name):
        PackageProxy.__init__(self, '%s.mus.chunks' % purview_package_short_name)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (self.class_name, self.purview.package_short_name)

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

    def list_chunk_directories(self):
        chunk_directories = []
        for x in self.list_chunk_package_short_names():
            directory = os.path.join(self.directory_name, x)
            chunk_directories.append(directory)
        return chunk_directories

    def list_chunk_package_short_names(self):
        chunk_package_short_names = os.listdir(self.directory_name)
        chunk_package_short_names = [x for x in chunk_package_short_names if x[0].isalpha()]
        return chunk_package_short_names

    def list_chunk_spaced_names(self):
        chunk_spaced_names = []
        for chunk_package_short_name in self.list_chunk_package_short_names():
            chunk_spaced_name = chunk_package_short_name.replace('_', ' ')
            chunk_spaced_names.append(chunk_spaced_name)
        return chunk_spaced_names

    def list_chunk_underscored_names(self):
        return self.list_chunk_package_short_names()

    # TODO: implement me
    def manage_chunks(self):
        self.print_not_implemented()
