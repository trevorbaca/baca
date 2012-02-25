from scf.proxies.PackageProxy import PackageProxy


class HomePackageProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, 
            package_importable_name=self.home_package_importable_name, 
            session=session)
