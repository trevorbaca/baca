from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.wranglers.AssetWrangler import AssetWrangler
import os


class PackageWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_external_wrangled_package_importable_names(self):
        result = []
        if self.score_external_wrangler_target_package_importable_name:
            wrangler_target_directory_name = self.package_importable_name_to_directory_name(
                self.score_external_wrangler_target_package_importable_name)
            for name in os.listdir(wrangler_target_directory_name):
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

    def fix_visible_wrangled_package_structures(self, prompt=True):
        results = []
        for package_proxy in self.list_visible_wrangled_asset_proxies():
            results.append(package_proxy.fix_package_structure(is_interactive=prompt))
            if prompt:
                package_proxy.profile_package_structure()
        return results

    def get_wrangled_asset_proxy(self, asset_full_name):
        return PackageProxy(asset_full_name, session=self.session)

    def list_score_internal_wrangled_package_directory_names(self, head=None):
        result = []
        for package_importable_name in self.list_score_internal_wrangled_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    def list_score_internal_wrangled_package_importable_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_wrangler_target_package_importable_names(head=head):
            if self.score_internal_wrangler_target_package_importable_name_suffix:
                package_directory_name = self.package_importable_name_to_directory_name(
                    package_importable_name)
                for name in os.listdir(package_directory_name):
                    if name[0].isalpha():
                        result.append('{}.{}'.format(package_importable_name, name))
            else:
                result.append(package_importable_name)
        return result

    def list_visible_wrangled_package_short_names(self, head=None):
        result = []
        for package_proxy in self.list_visible_wrangled_asset_proxies(head=head):
            result.append(package_proxy.package_short_name)
        return result

    def list_visible_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_visible_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def list_wrangled_asset_menuing_pairs(self, head=None):
        keys = self.list_wrangled_package_importable_names(head=head)
        bodies = self.list_wrangled_package_spaced_names(head=head)
        return zip(keys, bodies)

    def list_wrangled_asset_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_wrangled_package_importable_names(head=head):
            wrangled_package_proxy = self.get_wrangled_asset_proxy(package_importable_name)
            result.append(wrangled_package_proxy)
        return result

    def list_wrangled_package_directory_names(self, head=None):
        result = []
        for package_importable_name in self.list_wrangled_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    def list_wrangled_package_importable_names(self, head=None):
        if head is None: head = ''
        result, package_importable_names = [], []
        package_importable_names.extend(self.score_external_wrangled_package_importable_names)
        package_importable_names.extend(
            self.list_score_internal_wrangled_package_importable_names(head=head))
        for package_importable_name in package_importable_names:
            if package_importable_name.startswith(head):
                result.append(package_importable_name)
        return result

    def list_wrangled_package_short_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_importable_names(head=head):
            result.append(x.split('.')[-1])
        return result

    def list_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def make_wrangled_asset(self, package_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(package_short_name)
        package_directory_name = os.path.join(self.current_wrangler_target_directory_name, package_short_name)
        os.mkdir(package_directory_name)
        package_proxy = self.get_wrangled_asset_proxy(package_short_name)
        package_proxy.fix_package_structure(is_interactive=False)

    def profile_visible_assets(self):
        for package_proxy in self.list_visible_wrangled_asset_proxies():
            package_proxy.profile_package_structure()
