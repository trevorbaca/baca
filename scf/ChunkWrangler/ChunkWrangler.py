from abjad.tools import iotools
from baca.scf.ChunkProxy import ChunkProxy
from baca.scf.PackageProxy import PackageProxy
import inspect
import os


class ChunkWrangler(PackageProxy):

    def __init__(self, package_importable_name):
        PackageProxy.__init__(self, package_importable_name)

    ### PUBLIC METHODS ###

    def create_chunk_interactively(self, menu_header=None):
        chunk_proxy = self.ChunkProxy()
        chunk.purview = self.purview
        chunk_proxy.create_chunk_interactively()

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
