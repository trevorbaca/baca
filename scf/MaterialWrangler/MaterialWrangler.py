from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class MaterialWrangler(PackageWrangler, PackageProxy):

    def __init__(self, purview_package_short_name, session=None):
        if purview_package_short_name == 'baca':
            package_importable_name = '{}.materials'.format(purview_package_short_name)
        else:   
            package_importable_name = '{}.mus.materials'.format(purview_package_short_name)
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)

    ### PUBLIC ATTRIBUTES ###

    # TODO: remove
    @property
    def InteractiveMaterialProxy(self):
        import baca
        return baca.scf.InteractiveMaterialProxy

    # TODO: remove
    @property
    def StaticMaterialProxy(self):
        import baca
        return baca.scf.StaticMaterialProxy

    @property
    def breadcrumb(self):
        return 'materials'

    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def create_interactive_material_package_interactively(self):
        interactive_material_proxy = self.InteractiveMaterialPackage(package_importable_name)
        interactive_material_proxy.create_interactively()

    def create_static_material_package_interactively(self):
        static_material_package_proxy = self.StaticMaterialProxy()
        static_material_package_proxy.create_interactively()

    def get_package_proxy(self, package_importable_name):
        import baca
        package_proxy = baca.scf.PackageProxy(package_importable_name)
        if package_proxy.has_tag('maker'):
            return self.InteractiveMaterialProxy(package_importable_name)
        else:
            return self.StaticMaterialProxy(package_importable_name)

    def handle_main_menu_result(self, result):
        if result == 'i':
            menu_title = menu.menu_title
            self.material_wrangler.create_interactive_material_package_interactively()
        elif result == 's':
            menu_title = menu.menu_title
            self.material_wrangler.create_static_material_interactively(menu_title=menu_title)
        else:
            material_proxy = self.make_material_proxy(result)
            material_proxy.run()
        
    def iterate_material_summaries(self):
        for material_proxy in self.iterate_package_proxies():
            summary = material_proxy.package_short_name
            if not material_proxy.has_tag('maker'):
                summary = summary + ' (@)'
            yield summary

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.menu_entry_tokens = list(self.iterate_material_summaries())
        section.return_value_attr = 'body'
        section = menu.make_new_section()
        section.append(('i', 'create interactive material'))
        section.append(('s', 'create static material'))
        return menu

    # TODO: remove the need to strip these indicators
    def make_material_proxy(self, material_underscored_name):
        #score_package_importable_name = 'baca.materials'
        score_package_importable_name = self.package_importable_name
        package_importable_name_parts = []
        package_importable_name_parts.append(score_package_importable_name)
        package_importable_name_parts.append(material_underscored_name.strip(' (@)'))
        package_importable_name = '.'.join(package_importable_name_parts)
        if material_underscored_name.endswith('(@)'):
            material_proxy = self.StaticMaterialProxy(package_importable_name, session=self.session)
        else:
            material_proxy = self.InteractiveMaterialProxy(package_importable_name, session=self.session)
        return material_proxy

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run()
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
