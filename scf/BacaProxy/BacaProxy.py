from baca.scf.PackageProxy import PackageProxy


class BacaProxy(PackageProxy):
    
    def __init__(self):
        PackageProxy.__init__(self, 'baca')

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_score_local_purview(self):
        return False

    @property
    def is_studio_global_purview(self):
        return True

    @property
    def materials_package_importable_name(self):
        return 'baca.materials' 
