from baca.scf.DirectoryProxy import DirectoryProxy
import os


class PackageProxy(DirectoryProxy):

    ### PUBLIC ATTRIBUTES ###

    @property
    def initializer(self):
        return os.path.join(self.directory, '__init__.py')

    @property
    def parent_initializer(self):
        return os.path.join(self.parent_directory, '__init__.py')
