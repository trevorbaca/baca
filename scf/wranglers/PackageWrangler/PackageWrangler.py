from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class PackageWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def temporary_asset_short_name(self):
        return '__temporary_package'
    
    @property
    def wrangled_asset_class(self):
        return PackageProxy

    ### PUBLIC METHODS ###

    def list_wrangled_asset_menuing_pairs(self, head=None):
        keys = self.list_visible_asset_importable_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)

    def list_wrangled_asset_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_wrangled_asset_importable_names(head=head):
            wrangled_package_proxy = self.get_wrangled_asset_proxy(package_importable_name)
            result.append(wrangled_package_proxy)
        return result

    def list_wrangled_asset_importable_names(self, head=None):
        if head is None: head = ''
        result, package_importable_names = [], []
        package_importable_names.extend(self.score_external_wrangled_asset_importable_names)
        package_importable_names.extend(
            self.list_score_internal_wrangled_asset_importable_names(head=head))
        for package_importable_name in package_importable_names:
            if package_importable_name.startswith(head):
                result.append(package_importable_name)
        return result

    def list_wrangled_package_short_names(self, head=None):
        result = []
        for x in self.list_wrangled_asset_importable_names(head=head):
            result.append(x.split('.')[-1])
        return result

    def list_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def make_wrangled_asset(self, asset_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(asset_short_name)
        asset_path_name = os.path.join(self.current_asset_container_path_name, asset_short_name)
        os.mkdir(asset_path_name)
        package_proxy = self.get_wrangled_asset_proxy(asset_short_name)
        package_proxy.fix(is_interactive=False)
