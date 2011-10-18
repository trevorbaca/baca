from baca.scf.PackageProxy import PackageProxy


class ChunkProxy(PackageProxy):

    ### PUBLIC METHODS ###

    def create_chunk(self):
        self.create_directory()
        self.create_initializer()
        self.proceed()
