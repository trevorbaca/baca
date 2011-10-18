from baca.scf.DirectoryProxy import DirectoryProxy
import os


class PackageWrangler(DirectoryProxy):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PackageProxy(self):
        import baca
        return baca.scf.PackageProxy

    ### PUBLIC METHODS ###

    def get_package_proxy(self, package_importable_name):
        return self.PackageProxy(package_importable_name, session=self.session)

    def iterate_package_importable_names(self):
        for package_proxy in self.iterate_package_proxies():
            yield package_proxy.package_importable_name

    def iterate_package_short_names(self):
        for package_proxy in self.iterate_package_proxies():
            yield package_proxy.package_short_name

    def iterate_package_proxies(self):
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
                        yield package_proxy

    def iterate_package_spaced_names(self):
        for package_proxy in self.iterate_package_proxies():
            yield package_proxy.package_spaced_name

    def iterate_package_underscored_names(self):
        return self.iterate_package_short_names()
