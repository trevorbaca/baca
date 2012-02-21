from abjad.tools import iotools
from baca.scf.proxies.FileProxy import FileProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def wrangled_asset_class(self):
        return FileProxy
