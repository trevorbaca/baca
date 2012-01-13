from abjad.tools import iotools
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.MaterialProxy import MaterialProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.StaticMaterialProxy import StaticMaterialProxy
import os


class MaterialWrangler(PackageWrangler, PackageProxy):

    # TODO: get rid of the idea that wranglers have a purview; always grant effective global purview
    def __init__(self, purview_package_short_name, session=None):
        import baca
        if purview_package_short_name == 'baca':
            package_importable_name = '{}.materials'.format(purview_package_short_name)
        else:   
            package_importable_name = '{}.mus.materials'.format(purview_package_short_name)
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)
        self._maker_wrangler = baca.scf.MakerWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'materials'

    # TODO: write test
    @property   
    def global_materials_directory_name(self):
        return os.path.join([self.global_directory_name, 'materials'])

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

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

    # TODO: write test
    def create_data_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        editor_class_name = None
        has_illustration = False
        self.create_material_package(material_package_importable_name, editor_class_name, has_illustration)

    # TODO: write test
    def create_editable_material_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        breadcrumbs = self.session.breadcrumbs[:]
        self.session.breadcrumbs[:] = []
        editor = self.maker_wrangler.select_maker_interactively(should_clear_terminal=False)
        self.session.breadcrumbs = breadcrumbs[:]
        editor_class_name = editor.class_name
        # TODO: set following attribute by editor automatically
        has_illustration = True
        self.create_material_package(material_package_importable_name, editor_class_name, has_illustration)

    # TODO: write test
    def create_handmade_material_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        editor_class_name = None
        has_illustration = True
        self.create_material_package(material_package_importable_name, editor_class_name, has_illustration)

    # TODO: write test
    def create_material_package(self, material_package_importable_name, editor_class_name, has_illustration,
        prompt_proceed=True):
        '''True on success.'''
        assert iotools.is_underscore_delimited_lowercase_package_name(material_package_importable_name)
        assert editor_class_name is None or iotools.is_uppercamelcase_string(editor_class_name)
        assert isinstance(has_illustration, bool)
        directory_name = self.package_importable_name_to_directory_name(material_package_importable_name)
        if os.path.exists(directory_name):
            if prompt_proceed:
                line = 'package {!r} already exists.'.format(material_name)
                self.proceed(lines=[line])
            return False
        os.mkdir(directory_name)
        material_proxy = MaterialProxy(material_package_importable_name, session=self.session)
        material_proxy.write_stub_initializer_to_disk()
        if editor_class_name is None:
#            is_data_only = not has_illustration
#            if is_data_only:
#                material_proxy.write_stub_data_material_definition_to_disk()
#            else:
#                material_proxy.write_stub_music_material_definition_to_disk()
            material_proxy.write_stub_material_definition_to_disk()
        material_proxy.add_tag('editor_class_name', editor_class_name)
        material_proxy.add_tag('has_illustration', has_illustration)
        if prompt_proceed:
            line = 'package {!r} created.'.format(material_package_importable_name)
            self.proceed(lines=[line])
        return True

    # TODO: write test
    def get_new_material_package_importable_name_interactively(self):
        import baca
        getter = self.make_new_getter(where=self.where())
        getter.append_string('material name')
        material_name = getter.run()
        if self.backtrack():
            return
        material_package_short_name = iotools.string_to_strict_directory_name(material_name)
        studio = baca.scf.Studio(session=self.session)
        self.preserve_backtracking = True
        purview_name = studio.get_purview_interactively()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        materials_package_importable_name = \
            self.purview_name_to_materials_package_importable_name(purview_name)
        material_package_importable_name = '{}.{}'.format(
            materials_package_importable_name, material_package_short_name)
        if self.material_package_exists(material_package_importable_name):
            line = 'Material package {!r} already exists.'.format(material_package_importable_name)
            self.proceed(lines=[line])
            return
        return material_package_importable_name

    def get_package_proxy(self, package_importable_name):
        package_proxy = PackageProxy(package_importable_name, session=self.session)
        if package_proxy.has_tag('maker'):
            return InteractiveMaterialProxy(package_importable_name, session=self.session)
        else:
            return StaticMaterialProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.create_data_package_interactively()
        elif result == 'h':
            self.create_handmade_material_package_interactively()
        elif result == 'e':
            self.create_editable_material_package_interactively()
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
        section.tokens = list(self.iterate_material_summaries())
        section.return_value_attribute = 'body'
        section = menu.make_new_section()
        section.append(('d', 'make data'))
        section.append(('h', 'make material by hand'))
        section.append(('e', 'make material with editor'))
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

    # TODO: write test
    def material_package_exists(self, material_package_importable_name):
        try:
            MaterialProxy(material_package_importable_name)
            return True
        except:
            return False

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
