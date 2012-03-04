from scf.selectors.Selector import Selector


class MaterialPackageSelector(Selector):

	### CLASS ATTRIBUTES ###

    asset_subtree_package_importable_names = []
    target_human_readable_name = 'material package'

    ### PUBLIC METHODS ###

    def list_material_package_path_names(self):
        result = []
        for asset_subtree_package_importable_name in self.asset_subtree_package_importable_names:
            for package_path_name in self.list_public_package_path_names_in_subtree(
                asset_subtree_package_importable_name):
                if self.get_tag_from_path_name(package_path_name, 'material_type') == self.material_type:
                    result.append(package_path_name)
        return result
