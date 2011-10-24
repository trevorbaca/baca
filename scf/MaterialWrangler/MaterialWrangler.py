from baca.scf.PackageProxy import PackageProxy
import os


class MaterialWrangler(PackageProxy):

    def __init__(self, purview_package_short_name):
        if purview_package_short_name == 'baca':
            PackageProxy.__init__(self, '%s.materials' % purview_package_short_name)
        else:   
            PackageProxy.__init__(self, '%s.mus.materials' % purview_package_short_name)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (self.class_name, self.purview.package_short_name)

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

    def get_material_proxy(self, package_importable_name):
        package_proxy = PackageProxy(package_importable_name)
        if package_proxy.has_tag('maker'):
            return self.InteractiveMaterialProxy(package_importable_name)
        else:
            return self.StaticMaterialProxy(package_importable_name)

    def iterate_material_package_importable_names(self):
        for material_proxy in self.iterate_material_proxies():
            yield material_proxy.package_importable_name

    def iterate_material_package_short_names(self):
        for material_proxy in self.iterate_material_proxies():
            yield material_proxy.package_short_name

    def iterate_material_proxies(self):
        for x in os.listdir(self.directory_name):
            if x[0].isalpha():
                directory = os.path.join(self.directory_name, x)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        package_importable_name = '%s.%s' % (self.purview.materials_package_importable_name, x)
                        material_proxy = self.get_material_proxy(package_importable_name)
                        yield material_proxy

    def iterate_material_spaced_names(self):
        for material_proxy in self.iterate_material_proxies():
            yield material_proxy.material_spaced_name
        
    def iterate_material_summaries(self):
        for material_proxy in self.iterate_material_proxies():
            summary = material_proxy.package_short_name
            if not material_proxy.has_tag('maker'):
                summary = summary + ' (@)'
            yield summary

    def iterate_material_underscored_names(self):
        return self.iterate_material_package_short_names()

    def manage_materials(self, menu_header=None, command_string=None):
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'shared materials'
            menu.items_to_number = list(self.iterate_material_summaries())
            menu.sentence_length_items.append(('i', 'create interactive material'))
            menu.sentence_length_items.append(('s', 'create static material'))
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
