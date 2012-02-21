from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class PackageWrangler(AssetWrangler):

    def get_wrangled_asset_proxy(self, asset_full_name):
        return PackageProxy(asset_full_name, session=self.session)
