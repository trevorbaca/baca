from scf.proxies.FileProxy import FileProxy


class IllustrationLyFileProxy(FileProxy):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def extension(self):
        return '.ly'
