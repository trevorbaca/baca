from abjad.tools import iotools
from baca.scf.proxies.FileProxy import FileProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, asset_full_name):
        return FileProxy(asset_full_name, session=self.session)
