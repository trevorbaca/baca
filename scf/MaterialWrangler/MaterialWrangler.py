from baca.scf.PackageWrangler import PackageWrangler
import os


class MaterialWrangler(PackageWrangler):

    def __init__(self, purview_package_short_name):
        if purview_package_short_name == 'baca':
            package_importable_name = '%s.materials' % purview_package_short_name
        else:   
            package_importable_name = '%s.mus.materials' % purview_package_short_name
        self.package_importable_name = package_importable_name
        directory_name = self.package_importable_name_to_directory_name(self.package_importable_name)
        PackageWrangler.__init__(self, directory_name=directory_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def InteractiveMaterialProxy(self):
        import baca
        return baca.scf.InteractiveMaterialProxy

    @property
    def StaticMaterialProxy(self):
        import baca
        return baca.scf.StaticMaterialProxy

    ### PUBLIC METHODS ###

    def create_interactive_material_package_interactively(self, menu_header=None):
        interactive_material_proxy = self.InteractiveMaterialPackage(package_importable_name)
        interactive_material_proxy.create_interactively()

    def create_static_material_package_interactively(self, menu_header=None):
        static_material_package_proxy = self.StaticMaterialProxy()
        static_material_package_proxy.create_interactively()

    def get_package_proxy(self, package_importable_name):
        import baca
        package_proxy = baca.scf.PackageProxy(package_importable_name)
        if package_proxy.has_tag('maker'):
            return self.InteractiveMaterialProxy(package_importable_name)
        else:
            return self.StaticMaterialProxy(package_importable_name)

    def iterate_material_summaries(self):
        for material_proxy in self.iterate_package_proxies():
            summary = material_proxy.package_short_name
            if not material_proxy.has_tag('maker'):
                summary = summary + ' (@)'
            yield summary

    def manage_materials(self, menu_header=None, command_string=None):
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'shared materials'
            menu_section = self.MenuSection()
            menu_section.items_to_number = list(self.iterate_material_summaries())
            menu_section.sentence_length_items.append(('i', 'create interactive material'))
            menu_section.sentence_length_items.append(('s', 'create static material'))
            menu.menu_sections.append(menu_section)
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'i':
                menu_title = menu.menu_title
                self.material_wrangler.create_interactive_material_package_interactively(
                    menu_header=menu_title)
            elif key == 's':
                menu_title = menu.menu_title
                self.material_wrangler.create_static_material_interactively(menu_title=menu_title)
            else:
                score_package_importable_name = 'baca.materials'
                material_underscored_name = value
                if material_underscored_name.endswith('(@)'):
                    package_importable_name = '%s.%s' % (
                        score_package_importable_name, material_underscored_name.strip(' (@)'))
                    material_proxy = self.StaticMaterialProxy(package_importable_name)
                else:
                    package_importable_name = '%s.%s' % (score_package_importable_name, material_underscored_name)
                    material_proxy = self.InteractiveMaterialProxy(package_importable_name)
                material_proxy.score_title = 'Materials'
                material_proxy.manage_material(menu_header=menu.menu_title)
