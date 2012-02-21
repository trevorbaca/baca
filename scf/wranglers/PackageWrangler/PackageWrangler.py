from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class PackageWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_external_wrangled_package_directory_names(self):
        result = []
        for package_importable_name in self.score_external_wrangled_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    @property
    def score_external_wrangled_package_importable_names(self):
        result = []
        if self.score_external_wrangler_target_package_importable_name is not None:
            global_package_directory_name = self.package_importable_name_to_directory_name(
                self.score_external_wrangler_target_package_importable_name)
            for name in os.listdir(global_package_directory_name):
                if name[0].isalpha():
                    result.append('{}.{}'.format(
                        self.score_external_wrangler_target_package_importable_name, name))
        return result

    @property
    def temporary_package_directory_name(self):
        return os.path.join(self.current_wrangler_target_directory_name, '__temporary_package')

    @property
    def temporary_package_importable_name(self):
        package_path = self.current_wrangler_target_package_importable_name
        if package_path:
            return self.dot_join([package_path, '__temporary_package'])
        else:
            return '__temporary_package'

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, asset_full_name):
        return PackageProxy(asset_full_name, session=self.session)
