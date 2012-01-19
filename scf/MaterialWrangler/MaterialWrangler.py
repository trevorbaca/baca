from abjad.tools import iotools
from baca.scf.MaterialProxy import MaterialProxy 
from baca.scf.PackageWrangler import PackageWrangler
import collections
import os


class MaterialWrangler(PackageWrangler):

    def __init__(self, session=None):
        import baca
        PackageWrangler.__init__(self, 
            self.studio_materials_package_importable_name, 'mus.materials', session=session)
        self._material_proxy_wrangler = baca.scf.MaterialProxyWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'materials'

    @property
    def material_proxy_wrangler(self):
        return self._material_proxy_wrangler
    
    ### PUBLIC METHODS ###

    # TODO: write test
    def make_data_package_interactively(self):
        self.preserve_backtracking = True
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        user_input_handler_class_name = None
        should_have_illustration = False
        self.make_material_package(material_package_importable_name, user_input_handler_class_name, should_have_illustration)

    # TODO: write test
    def make_editable_material_package_interactively(self):
        self.preserve_backtracking = True
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        self.preserve_backtracking = True
        breadcrumbs = self.session.breadcrumbs[:]
        self.session.breadcrumbs[:] = []
        user_input_handler_class_name = \
            self.material_proxy_wrangler.select_material_proxy_class_name_interactively(
            clear=False, cache=True)
        self.session.breadcrumbs = breadcrumbs[:]
        self.preserve_backtracking = False
        if self.backtrack():
            return
        # TODO: set following attribute by editor automatically
        should_have_illustration = True
        self.make_material_package(
            material_package_importable_name, user_input_handler_class_name, should_have_illustration)

    # TODO: write test
    def make_handmade_material_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        user_input_handler_class_name = None
        should_have_illustration = True
        self.make_material_package(material_package_importable_name, user_input_handler_class_name, should_have_illustration)

    # TODO: write test
    def make_material_package(self, material_package_importable_name, user_input_handler_class_name, 
        should_have_illustration, prompt=True):
        '''True on success.'''
        assert iotools.is_underscore_delimited_lowercase_package_name(material_package_importable_name)
        assert user_input_handler_class_name is None or iotools.is_uppercamelcase_string(
            user_input_handler_class_name)
        assert isinstance(should_have_illustration, bool)
        directory_name = self.package_importable_name_to_directory_name(material_package_importable_name)
        if os.path.exists(directory_name):
            line = 'package {!r} already exists.'.format(material_name)
            self.proceed(line, prompt=prompt)
            return False
        os.mkdir(directory_name)
        material_proxy = MaterialProxy(material_package_importable_name, session=self.session)
        tags = collections.OrderedDict([])
        tags['user_input_handler_class_name'] = user_input_handler_class_name
        tags['should_have_illustration'] = should_have_illustration
        material_proxy.write_stub_initializer_to_disk(tags=tags)
        if user_input_handler_class_name is None:
            if should_have_illustration:
                material_proxy.write_stub_music_material_definition_to_disk()
                material_proxy.write_stub_illustration_builder_to_disk(prompt=False)
            else:
                material_proxy.write_stub_data_material_definition_to_disk()
        line = 'material package {!r} created.'.format(material_package_importable_name)
        self.proceed(line, prompt=prompt)
        return True

    # TODO: write test
    def get_new_material_package_importable_name_interactively(self):
        import baca
        getter = self.make_new_getter(where=self.where())
        getter.append_string('material name')
        self.preserve_backtracking = True
        material_name = getter.run()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        material_package_short_name = iotools.string_to_strict_directory_name(material_name)
        studio = baca.scf.Studio(session=self.session)
        self.preserve_backtracking = True
        purview_name = studio.get_purview_interactively(clear=False)
        self.preserve_backtracking = False
        if self.backtrack():
            return
        materials_package_importable_name = \
            self.purview_name_to_materials_package_importable_name(purview_name)
        material_package_importable_name = '{}.{}'.format(
            materials_package_importable_name, material_package_short_name)
        if self.package_exists(material_package_importable_name):
            line = 'Material package {!r} already exists.'.format(material_package_importable_name)
            self.proceed(line)
            return
        return material_package_importable_name

    def get_package_proxy(self, package_importable_name):
        return self.material_proxy_wrangler.get_package_proxy(package_importable_name)

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 'h':
            self.make_handmade_material_package_interactively()
        elif result == 'e':
            self.make_editable_material_package_interactively()
        else:
            material_proxy = self.get_package_proxy(result)
            material_proxy.run()
        
    def make_main_menu(self, head=None):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True, is_keyed=False)
        section.tokens = self.list_wrangled_package_menuing_pairs(head=head)
        section = menu.make_new_section()
        section.append(('d', 'make data'))
        section.append(('h', 'make material by hand'))
        section.append(('e', 'make material with editor'))
        return menu

    # TODO: write tests
    def purview_name_to_materials_package_importable_name(self, purview_name):
        assert isinstance(purview_name, str)
        result = []
        result.append(purview_name)
        if not purview_name == self.studio_package_importable_name:
            result.append('mus')
        result.append('materials')
        result = '.'.join(result)
        return result

    def run(self, user_input=None, head=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
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
        self.restore_breadcrumbs(cache=cache)
