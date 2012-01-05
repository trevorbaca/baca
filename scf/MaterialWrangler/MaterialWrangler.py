from abjad.tools import iotools
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.StaticMaterialProxy import StaticMaterialProxy
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

#    def create_interactive_material_package_interactively(self):
#        interactive_material_proxy = InteractiveMaterialProxy(package_importable_name, session=self.session)
#        interactive_material_proxy.create_interactively()
#
#    def create_static_material_package_interactively(self):
#        static_material_package_proxy = StaticMaterialProxy(session=self.session)
#        static_material_package_proxy.create_interactively()

    def create_material_package_interactively(self):
        import baca
        getter = self.make_new_getter(where=self.where())
        getter.append_string('material name')
        material_name = getter.run()
        if self.backtrack():
            return
        directory_name = iotools.string_to_strict_directory_name(material_name)
        studio = baca.scf.Studio(session=self.session)
        menu = studio.make_score_selection_menu()
        menu.sections[-1].menu_entry_tokens.append(('outside', 'store outside score')) 
        menu.explicit_title = 'select {} location:'.format(material_name)
        result = menu.run(should_clear_terminal=False)
        if self.backtrack():
            return
        purview = result
        line = 'data gathered so far: {!r} and {!r}.'.format(material_name, purview)
        self.proceed(lines=[line])

    def get_package_proxy(self, package_importable_name):
        package_proxy = PackageProxy(package_importable_name, session=self.session)
        if package_proxy.has_tag('maker'):
            return InteractiveMaterialProxy(package_importable_name, session=self.session)
        else:
            return StaticMaterialProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.create_material_package_interactively()
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
        section.append(('new', 'make new material'))
        return menu

    # TODO: remove the need to strip these indicators
    def make_material_proxy(self, material_underscored_name):
        score_package_importable_name = self.package_importable_name
        package_importable_name_parts = []
        package_importable_name_parts.append(score_package_importable_name)
        package_importable_name_parts.append(material_underscored_name.strip(' (@)'))
        package_importable_name = '.'.join(package_importable_name_parts)
        if material_underscored_name.endswith('(@)'):
            material_proxy = StaticMaterialProxy(package_importable_name, session=self.session)
        else:
            material_proxy = InteractiveMaterialProxy(package_importable_name, session=self.session)
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
