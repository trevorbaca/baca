from baca.scf.wranglers.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
from baca.scf.wranglers.MaterialPackageWrangler import MaterialPackageWrangler
from baca.scf.proxies.PackageProxy import PackageProxy


class HomePackageProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, self.home_package_importable_name, session=session)
        self._material_package_maker_wrangler = MaterialPackageMakerWrangler(session=self.session)
        self._material_package_wrangler = MaterialPackageWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler
  
    @property
    def current_materials_package_importable_name(self):
        return self.score_external_materials_package_importable_name
