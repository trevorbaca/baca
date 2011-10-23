from baca.scf.PackageProxy import PackageProxy


class BacaProxy(PackageProxy):
    
    def __init__(self):
        PackageProxy.__init__(self, 'baca')

    ### PUBLIC ATTRIBUTES ###

    @property
    def materials_package_importable_name(self):
        return 'baca.materials' 
