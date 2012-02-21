from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class ImportableAssetWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_external_wrangled_asset_importable_names(self):
        result = []
        for short_name in self.score_external_wrangled_asset_short_names:
            result.append('{}.{}'.format(self.score_external_asset_container_importable_name, short_name))
        return result

    @property
    def temporary_asset_importable_name(self):
        if self.current_asset_container_importable_name:
            return self.dot_join([
                self.current_asset_container_importable_name,
                self.temporary_asset_short_name])
        else:
            return self.temporary_asset_short_name

    ### PUBLIC METHODS ###

    def list_score_internal_wrangled_asset_importable_names(self, head=None):
        result = []
        for asset_container_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            if self.score_internal_asset_container_importable_name_infix:
                asset_path_name = self.package_importable_name_to_path_name(
                    asset_container_importable_name)
                for name in os.listdir(asset_path_name):
                    if name[0].isalpha():
                        result.append('{}.{}'.format(asset_container_importable_name, name))
            else:
                result.append(asset_container_importable_name)
        return result

    def list_visible_asset_importable_names(self, head=None):
        result = []
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.importable_name)
        return result
