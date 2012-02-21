from baca.scf.wranglers.AssetWrangler import AssetWrangler


class ImportableAssetWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_external_wrangled_asset_importable_names(self):
        result = []
        for short_name in self.score_external_wrangled_asset_short_names:
            result.append('{}.{}'.format(self.score_external_asset_container_importable_name, short_name))
        return result
