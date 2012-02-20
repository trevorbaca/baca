from baca.scf.proxies.PackageProxy import PackageProxy


class HomePackageProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, self.home_package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def current_materials_package_importable_name(self):
        return self.score_external_materials_package_importable_name
