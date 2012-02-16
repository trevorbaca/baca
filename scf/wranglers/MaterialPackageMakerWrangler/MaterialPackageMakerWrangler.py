from abjad.tools import iotools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from baca.scf.wranglers.PackageWrangler import PackageWrangler
import os


class MaterialPackageMakerWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, self.materialpackagemakers_package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'material proxies'

    @property
    def material_proxy_spaced_class_names(self):
        result = []
        for name in self.list_wrangled_package_short_names(head=self.studio_package_importable_name):
            spaced_class_name = iotools.uppercamelcase_to_space_delimited_lowercase(name)
            result.append(spaced_class_name)
        result.remove('material package maker')
        return result

    ### PUBLIC METHODS ###

    def get_package_proxy(self, material_package_importable_name):
        import baca
        material_proxy = baca.scf.proxies.MaterialPackageProxy(material_package_importable_name, session=self.session)
        material_package_maker_class_name = material_proxy.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_proxy_class = None
            command = 'from baca.scf.materialpackagemakers import {} as material_proxy_class'
            command = command.format(material_package_maker_class_name)
            exec(command)
            material_proxy = material_proxy_class(material_package_importable_name, session=self.session)
        return material_proxy
            
    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_material_proxy_interactively()
        else:
            raise ValueError

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.material_proxy_spaced_class_names
        section = menu.make_section()
        section.append(('new', 'make material_proxy'))
        return menu

    # TODO: implement MaterialPackageProxyClassFile object to model and customize these settings
    def make_material_proxy_class_file(self, material_proxy_name, generic_output_name):
        class_file_name = os.path.join(
            self.toplevel_global_package_importable_name, material_proxy_name, material_proxy_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from baca.music.foo import foo')
        lines.append('from baca.music.foo import make_illustration_from_output_material')
        lines.append('from baca.scf.materialpackagemakers.MaterialPackageMaker import MaterialPackageMaker')
        lines.append('from baca.scf.editors.UserInputWrapper import UserInputWrapper')
        lines.append('import baca')
        lines.append('')
        lines.append('')
        lines.append('class {}(MaterialPackageMaker):'.format(material_proxy_name))
        lines.append('')
        lines.append('    def __init__(self, package_importable_name=None, session=None):')
        lines.append('        MaterialPackageMaker.__init__(')
        lines.append('            self, package_importable_name=package_importable_name, session=seession')
        lines.append('')
        lines.append('    ### READ-ONLY PUBLIC ATTRIBUTES ###')
        lines.append('')
        lines.append('    generic_output_name = {!r}'.format(generic_output_name))
        lines.append('')
        lines.append('    illustration_maker = staticmethod(make_illustration_from_output_material)')
        lines.append('')
        lines.append('    output_material_checker = staticmethod(componenttools.all_are_components)')
        lines.append('')
        lines.append('    output_material_maker = staticmethod(baca.music.foo)')
        lines.append('')
        lines.append('    output_material_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_demo_values = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_tests = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    ### PUBLIC METHODS ###')
        lines.append('')
        lines.append('    @property')
        lines.append('    def output_material_module_body_lines(self):')
        lines.append('        lines = []')
        lines.append('        output_material = self.output_material')
        lines.append("        lines.append('{} = {!r}'.format(self.material_underscored_name, output_material)")
        class_file.write('\n'.join(lines))
        class_file.close()

    # TODO: change to boilerplate file stored in material_proxy package
    def make_material_proxy_initializer(self, material_proxy_name):
        initializer_file_name = os.path.join(
            self.toplevel_global_package_importable_name, material_proxy_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools.importtools._import_structured_package import _import_structured_package\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("_import_structured_package(__path__[0], globals(), 'baca')\n")
        initializer.close() 

    def make_material_proxy_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('material proxy name')
        material_proxy_name = getter.run()
        if self.backtrack():
            return
        assert iotools.is_uppercamelcase_string(material_proxy_name)
        assert material_proxy_name.endswith('Maker')
        getter = self.make_getter(where=self.where())
        getter.append_string('generic output product')
        generic_output_product = getter.run()
        if self.backtrack():
            return
        material_proxy_directory = os.path.join(self.toplevel_global_package_importable_name, material_proxy_name)
        os.mkdir(material_proxy_directory)
        self.make_material_proxy_initializer(material_proxy_name)
        self.make_material_proxy_class_file(material_proxy_name, generic_output_product)
        self.make_material_proxy_stylesheet(material_proxy_name)


    # TODO: change to boilerplate file stored somewhere
    def make_material_proxy_stylesheet(self, material_proxy_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.makup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(
            self.toplevel_global_package_importable_name, material_proxy_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()
        
    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
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

    # TODO: write test
    def select_material_proxy_class_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.material_proxy_spaced_class_names
        while True:
            self.push_breadcrumb('select material proxy:')
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue 
            else:
                self.pop_breadcrumb()
                break
        material_proxy_class_name = iotools.space_delimited_lowercase_to_uppercamelcase(result) 
        self.restore_breadcrumbs(cache=cache)
        return material_proxy_class_name

    def unimport_materialpackagemakers_package(self):
        self.remove_package_importable_name_from_sys_modules(self.toplevel_global_package_importable_name)
