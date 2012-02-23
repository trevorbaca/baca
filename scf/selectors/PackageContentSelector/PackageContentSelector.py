from scf.selectors.DirectoryContentSelector import DirectoryContentSelector
import os


class PackageContentSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = []
    target_human_readable_name = 'item'

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.list_asset_classes()
        def fset(self, items):
            self._items = list(items)
        return property(**locals())

    ### PUBLIC METHODS ###

    def list_asset_classes(self):
        from scf.proxies.PackageProxy import PackageProxy
        result = []
        for package_importable_name in self.asset_container_package_importable_names:
            package_proxy = PackageProxy(
                package_importable_name=package_importable_name, session=self.session)
            result.extend(package_proxy.public_names)
        return result
