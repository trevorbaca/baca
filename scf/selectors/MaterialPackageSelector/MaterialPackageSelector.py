from scf.selectors.Selector import Selector


class MaterialPackageSelector(Selector):

	### CLASS ATTRIBUTES ###

    asset_subtree_package_importable_names = []
    target_human_readable_name = 'material package'

    ### PUBLIC METHODS ###

    def list_material_package_path_names(self):
        for asset_subtree_package_importable_name in self.asset_subtree_package_importable_names:
            pass
