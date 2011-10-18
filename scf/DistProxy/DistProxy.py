from baca.scf.DirectoryProxy import DirectoryProxy
import os


class DistProxy(DirectoryProxy):

    def __init__(self, score_package_short_name, session=None):
        directory_name = os.path.join(os.environ.get('SCORES'), score_package_short_name, 'dist')
        DirectoryProxy.__init__(self, directory_name, session=session)
