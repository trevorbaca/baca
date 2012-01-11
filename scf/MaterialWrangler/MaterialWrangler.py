from abjad.tools import iotools
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.MaterialProxy import MaterialProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.StaticMaterialProxy import StaticMaterialProxy
import os


class MaterialWrangler(PackageWrangler, PackageProxy):

    # TODO: get rid of the idea that wranglers have a purview
    def __init__(self, purview_package_short_name, session=None):
        if purview_package_short_name == 'baca':
            package_importable_name = '{}.materials'.format(purview_package_short_name)
        else:   
            package_importable_name = '{}.mus.materials'.format(purview_package_short_name)
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'materials'

    # TODO: write test
    @property   
    def global_materials_directory_name(self):
        return os.path.join([self.global_directory_name, 'materials'])

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    # TODO: remove this attribute entirely?
    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    ### PUBLIC METHODS ###

    # TODO: write tests
    # TODO: change signature to material_package_importable_name
    def create_material_package(self, purview_name, material_package_short_name):
        '''Package importable name on success. Change to just true on success.'''
        materials_package_importable_name = \
            self.purview_name_to_materials_package_importable_name(purview_name)
        material_package_importable_name = '{}.{}'.format(
            materials_package_importable_name, material_package_short_name)
        directory_name = self._package_importable_name_to_directory_name(material_package_importable_name)
        if os.path.exists(directory_name):
            return False
        os.mkdir(directory_name)
        self.write_initializer_to_package(material_package_importable_name)
        material_proxy = MaterialProxy(material_package_importable_name, session=self.session)
        material_proxy.write_stub_material_definition_to_disk()
        return material_package_importable_name

    # TODO: write tests
    def create_material_package_interactively(self):
        import baca
        getter = self.make_new_getter(where=self.where())
        getter.append_string('material name')
        material_name = getter.run()
        if self.backtrack():
            return
        studio = baca.scf.Studio(session=self.session)
        # TODO: encapsulate in self.get_purview_interactively() method and write tests
        while True:
            menu = studio.make_score_selection_menu()
            menu.sections[-1].menu_entry_tokens.append(('baca', 'store elsewhere')) 
            menu.explicit_title = 'select location for {!r}:'.format(material_name)
            purview_name = menu.run(should_clear_terminal=False)
            if self.backtrack():
                return
            if purview_name:
                break
        material_directory_name = iotools.string_to_strict_directory_name(material_name)
        result = self.create_material_package(purview_name, material_directory_name)
        if result:
            line = 'package {!r} created.'.format(result)
        else:
            line = 'package {!r} already exists.'.format(material_name)
        self.proceed(lines=[line])

#    def foo(self):
#        menu, section = self.make_new_menu()
#        menu.explicit_title = 'how will you create {!r}?'.format(material_name)
#        section.menu_entry_tokens.append(('h', 'by hand'))
#        section.menu_entry_tokens.append(('e', 'with editor'))
#        creation_mode = menu.run(should_clear_terminal=False)
#        if self.backtrack():
#            return
#        if creation_mode == 'h':
#            getter = self.make_new_getter()
#            getter.append_boolean('will you build a score to visualize {!r}?'.format(material_name)) 
#            build_score = getter.run()
#            if self.backtrack():
#                return
#        elif creation_mode == 'e':
#            studio = baca.scf.Studio(session=self.session)
#            maker_wrangler = baca.scf.MakerWrangler(session=self.session)
#            menu = maker_wrangler.make_maker_selection_menu()
#            menu.explicit_title = 'selct editor with which to create {!r}:'.format(material_name)
#            maker_package_short_name = menu.run()
#            if self.backtrack():
#                return
#            maker = maker_wrangler.get_maker(maker_package_short_name)
#            maker.run() # just guessing here; probably needs better consideration
#        else:
#            raise ValueError

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
        
    # TODO: change name to self.list_material_package_short_names
    def iterate_material_summaries(self):
        for material_proxy in self.iterate_package_proxies():
            summary = material_proxy.package_short_name
            yield summary

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.menu_entry_tokens = list(self.iterate_material_summaries())
        section.return_value_attribute = 'body'
        section = menu.make_new_section()
        section.append(('new', 'make new material'))
        return menu

    def make_material_proxy(self, material_underscored_name):
        score_package_importable_name = self.package_importable_name
        package_importable_name_parts = []
        package_importable_name_parts.append(score_package_importable_name)
        package_importable_name_parts.append(material_underscored_name)
        package_importable_name = '.'.join(package_importable_name_parts)
        package_proxy = PackageProxy(package_importable_name, session=self.session)
        if package_proxy.has_tag('maker'):
            material_proxy = InteractiveMaterialProxy(package_importable_name, session=self.session)
        else:
            material_proxy = StaticMaterialProxy(package_importable_name, session=self.session)
        return material_proxy

    # TODO: write tests
    def purview_name_to_materials_package_importable_name(self, purview_name):
        assert isinstance(purview_name, str)
        result = []
        result.append(purview_name)
        if not purview_name == 'baca':
            result.append('mus')
        result.append('materials')
        result = '.'.join(result)
        return result

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
