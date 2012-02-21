from abjad.tools import iotools
from baca.scf.proxies.ModuleProxy import ModuleProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class ModuleWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def wrangled_asset_class(self):
        return ModuleProxy
