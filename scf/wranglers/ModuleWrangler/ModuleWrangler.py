from abjad.tools import iotools
from baca.scf.proxies.ModuleProxy import ModuleProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class ModuleWrangler(AssetWrangler):

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, asset_full_name):
        return ModuleProxy(asset_full_name, session=self.session)
