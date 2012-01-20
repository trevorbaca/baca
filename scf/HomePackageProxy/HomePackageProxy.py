from baca.scf.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
from baca.scf.MaterialPackageWrangler import MaterialPackageWrangler
from baca.scf.PackageProxy import PackageProxy


class HomePackageProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, self.studio_package_importable_name, session=session)
        self._material_proxy_wrangler = MaterialPackageMakerWrangler(session=self.session)
        self._material_wrangler = MaterialPackageWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def is_score_local_purview(self):
        return False

    @property
    def is_studio_global_purview(self):
        return True

    @property
    def material_proxy_wrangler(self):
        return self._material_proxy_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler
  
    @property
    def materials_package_importable_name(self):
        return self.studio_materials_package_importable_name
