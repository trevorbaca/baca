from baca.scf.proxies.PackageProxy import PackageProxy


class HomePackageProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, self.home_package_importable_name, session=session)
