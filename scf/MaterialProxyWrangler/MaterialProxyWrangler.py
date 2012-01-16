from abjad.tools import iotools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class MaterialProxyWrangler(PackageWrangler, PackageProxy):

    def __init__(self, session=None):
        package_importable_name = 'baca.scf.materialproxies'
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)

    ### READ-ONLY PUBIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'material proxies'

    ### PUBLIC METHODS ###

    # TODO: write test
    def get_material_proxy(self, material_proxy_package_short_name, material_package_importable_name):
        command = 'from baca.scf.materialproxies import {} as material_proxy_class'.format(
            material_proxy_package_short_name)
        exec(command)
        material_proxy = material_proxy_class(
            material_package_importable_name=material_package_importable_name, session=self.session)
        return material_proxy

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_material_proxy()
        else:
            raise ValueError

    # TODO: write test
    def list_material_proxy_class_names(self):
        self.list_package_short_names()

    def list_material_proxy_spaced_class_names(self):
        result = []
        for package_short_name in self.list_package_short_names():
            spaced_class_name = iotools.uppercamelcase_to_space_delimited_lowercase(package_short_name)
            result.append(spaced_class_name)
        return result

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_material_proxy_spaced_class_names()
        section = menu.make_new_section()
        section.append(('new', 'make material_proxy'))
        return menu

    # replace with material_proxy wizard
    def make_material_proxy(self):
        while True:
            material_proxy_name = self.handle_raw_input('material_proxy name')
            if iotools.is_uppercamelcase_string(material_proxy_name):
                if material_proxy_name.endswith('Maker'):
                    break
        while True:
            generic_output_product = self.handle_raw_input('generic output product')
            break
        material_proxy_directory = os.path.join(self.directory_name, material_proxy_name)
        os.mkdir(material_proxy_directory)
        self.make_material_proxy_initializer(material_proxy_name)
        self.make_material_proxy_class_file(material_proxy_name, generic_output_product)
        self.make_material_proxy_stylesheet(material_proxy_name)

    # TODO: change to boilerplate file stored in material_proxy package
    def make_material_proxy_initializer(self, material_proxy_name):
        initializer_file_name = os.path.join(self.directory_name, material_proxy_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools.importtools._import_structured_package import _import_structured_package\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("_import_structured_package(__path__[0], globals(), 'baca')\n")
        initializer.close() 

    # TODO: implement MaterialProxyClassFile object to model and customize these settings
    def make_material_proxy_class_file(self, material_proxy_name, generic_output_name):
        class_file_name = os.path.join(self.directory_name, material_proxy_name, material_proxy_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from abjad.tools import lilypondfiletools')
        lines.append('from baca.scf.MaterialProxy import MaterialProxy')
        lines.append('from baca.scf.UserInputWrapper import UserInputWrapper')
        lines.append('import os')
        lines.append('')
        lines.append('')
        lines.append('class {}(MaterialProxy):'.format(material_proxy_name))
        lines.append('')
        lines.append('    def __init__(self, **kwargs):')
        lines.append('        MaterialProxy.__init__(self, **kwargs)')
        lines.append("        self._generic_output_name = {!r}".format(generic_output_name))
        lines.append('')
        lines.append('    ### READ-ONLY PUBLIC ATTRIBUTES ###')
        lines.append('')
        lines.append('    output_file_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_template = UserInputWrapper([')
        lines.append('        ])')
        lines.append('')
        lines.append('    ### PUBLIC METHODS ###')
        lines.append('')
        lines.append('    def get_output_file_lines(self, material, material_underscored_name):')
        lines.append('        output_file_lines = []')
        lines.append('        return output_file_lines')
        lines.append('')
        lines.append('    def make(self, foo, bar):')
        lines.append('        return material')
        lines.append('')
        lines.append('    def make_lilypond_file_from_output_material(self, material):')
        lines.append('        lilypond_file = lilypondfiletools.make_basic_lilypond_file()')
        lines.append('        return lilypond_file')
        class_file.write('\n'.join(lines))
        class_file.close()

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
        stylesheet_file_name = os.path.join(self.directory_name, material_proxy_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()
        
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

    # TODO: write test
    def select_material_proxy_class_name_interactively(self, should_clear_terminal=True):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_material_proxy_spaced_class_names()
        while True:
            self.append_breadcrumb('select material proxy:')
            result = menu.run(should_clear_terminal=should_clear_terminal)
            if self.backtrack():
                self.pop_breadcrumb()
                return
            elif not result:
                self.pop_breadcrumb()
                continue 
            else:
                self.pop_breadcrumb()
                break
        material_proxy_class_name = iotools.space_delimited_lowercase_to_uppercamelcase(result) 
        return material_proxy_class_name

    def unimport_materialproxies_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)
