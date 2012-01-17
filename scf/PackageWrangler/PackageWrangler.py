from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.PackageProxy import PackageProxy
import os


# TODO: replace with NewPackageWrangler
class PackageWrangler(DirectoryProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def has_packages(self):
        for x in self.package_spaced_names:
            return True
        return False

    @property
    def package_importable_names(self):
        result = []
        for package_proxy in self.package_proxies:
            result.append(package_proxy.package_importable_name)
        return result

    @property
    def package_proxies(self):
        result = []
        for x in os.listdir(self.directory_name):
            if x[0].isalpha():
                directory = os.path.join(self.directory_name, x)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        if hasattr(self, 'package_importable_name'):
                            package_importable_name = '{}.{}'.format(self.package_importable_name, x)
                        else:
                            package_importable_name = x
                        package_proxy = self.get_package_proxy(package_importable_name)
                        result.append(package_proxy)
        return result

    @property
    def package_short_names(self):
        result = []
        for package_proxy in self.package_proxies:
            result.append(package_proxy.package_short_name)
        return result

    @property
    def package_spaced_names(self):
        result = []
        for package_proxy in self.package_proxies:
            result.append(package_proxy.package_spaced_name)
        return result

    @property
    def package_underscored_names(self):
        return self.package_short_names

    ### PUBLIC METHODS ###

    def get_package_proxy(self, package_importable_name):
        return PackageProxy(package_importable_name, session=self.session)
