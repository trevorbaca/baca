from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.PackageProxy import PackageProxy


class BacaProxy(PackageProxy):
    
    def __init__(self):
        PackageProxy.__init__(self, 'baca')
        self._maker_wrangler = MakerWrangler()
        self._material_wrangler = MaterialWrangler('baca.materials')

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_score_local_purview(self):
        return False

    @property
    def is_studio_global_purview(self):
        return True

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler
  
    @property
    def materials_package_importable_name(self):
        return 'baca.materials' 
