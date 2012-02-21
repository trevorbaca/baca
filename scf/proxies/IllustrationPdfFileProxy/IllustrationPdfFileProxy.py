from baca.scf.proxies.FileProxy import FileProxy
import os


class IllustrationPdfFileProxy(FileProxy):

    ### PUBLIC METHODS ###

    def view(self):
        command = 'open {}'.format(self.path_name)
        os.system(command)
