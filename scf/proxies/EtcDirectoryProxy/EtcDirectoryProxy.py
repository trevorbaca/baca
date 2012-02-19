from baca.scf.proxies.DirectoryProxy import DirectoryProxy
import os


class EtcDirectoryProxy(DirectoryProxy):

    def __init__(self, score_package_short_name, session=None):
        directory_name = os.path.join(self.scores_directory_name, score_package_short_name, 'etc')
        DirectoryProxy.__init__(self, directory_name, session=session)
