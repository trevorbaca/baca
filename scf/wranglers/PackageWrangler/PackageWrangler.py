from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class PackageWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_external_asset_proxies(self):
        result = []
        for asset_path_name in self.score_external_asset_path_names:
            asset_package_importable_name = self.path_name_to_package_importable_name(asset_path_name)
            asset_proxy = self.get_asset_proxy(asset_package_importable_name)
            result.append(asset_proxy)
        return result

    @property
    def temporary_asset_short_name(self):
        return '__temporary_package'
    
    @property
    def asset_class(self):
        return PackageProxy

    ### PUBLIC METHODS ###

    # TODO: remove in favor of AssetWrangler.list_asset_huamn_readable_names()
    def list_asset_short_names(self, head=None):
        result = []
        for x in self.list_asset_importable_names(head=head):
            result.append(x.split('.')[-1])
        return result
        #return self.list_asset_human_readable_names(head=head)

    def make_asset(self, asset_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(asset_short_name)
        asset_path_name = os.path.join(self.current_asset_container_path_name, asset_short_name)
        os.mkdir(asset_path_name)
        package_proxy = self.get_asset_proxy(asset_short_name)
        package_proxy.fix(is_interactive=False)
