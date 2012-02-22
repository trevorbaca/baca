from abjad.tools import iotools
from baca.scf.proxies.ModuleProxy import ModuleProxy
from baca.scf.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class ModuleWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def asset_class(self):
        return ModuleProxy
