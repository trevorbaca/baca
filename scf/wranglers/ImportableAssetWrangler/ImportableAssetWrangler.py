from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class ImportableAssetWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    #@property
    #def score_external_asset_importable_names(self):
    def list_score_external_asset_importable_names(self, head=None):
        result = []
        if self.score_external_asset_container_path_name:
            for name in os.listdir(self.score_external_asset_container_path_name):
                if name[0].isalpha():
                    result.append(self.dot_join([self.score_external_asset_container_importable_name, name]))
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

    def list_score_internal_asset_importable_names(self, head=None):
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

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_importable_names(self, head=None):
        result = []
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.importable_name)
        return result

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_importable_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)

    def list_asset_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_asset_importable_names(head=head):
            asset_proxy = self.get_asset_proxy(package_importable_name)
            result.append(asset_proxy)
        return result

    def list_asset_importable_names(self, head=None):
        if head is None: head = ''
        result, asset_importable_names = [], []
        #asset_importable_names.extend(self.score_external_asset_importable_names)
        asset_importable_names.extend(self.list_score_external_asset_importable_names(head=head))
        asset_importable_names.extend(
            self.list_score_internal_asset_importable_names(head=head))
        for asset_importable_name in asset_importable_names:
            if asset_importable_name.startswith(head):
                result.append(asset_importable_name)
        return result
