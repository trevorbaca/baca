from baca.scf.DirectoryProxy import DirectoryProxy
import os


class ExgProxy(DirectoryProxy):

    def __init__(self, score_package_short_name):
        directory_name = os.path.join(os.environ.get('SCORES'), score_package_short_name, 'exg')
        DirectoryProxy.__init__(self, directory_name)
