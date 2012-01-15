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

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### READ-ONLY PUBIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'material proxies'

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    # TODO: make this read-only
    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def get_material_proxy(self, material_proxy_package_short_name):
        command = 'from baca.scf.materialproxies import {} as material_proxy_class'.format(material_proxy_package_short_name)
        exec(command)
        material_proxy = material_proxy_class()
        return material_proxy

    # replace with wrapped call to PackageWrangler.list_package_proxies()
    def list_material_proxys(self):
        self.unimport_baca_package()
        self.unimport_material_proxys_package()
        command = 'import baca'
        exec(command)
        for material_proxy_class_name in self.list_material_proxy_class_names():
            command = 'result = baca.scf.materialproxies.{}()'.format(material_proxy_class_name)
            exec(command)
            yield result

    # add PackageWrangler.list_package_class_names and replace this with it
    def list_material_proxy_class_names(self):
        material_proxy_directories = []
        for name in os.listdir(self.directory_name):
            if name[0].isalpha():
                directory = os.path.join(self.directory_name, name)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        material_proxy_directories.append(name)
        return material_proxy_directories

    def list_material_proxy_spaced_class_names(self):
        material_proxy_spaced_class_names = []
        for material_proxy in self.list_material_proxys():
            material_proxy_spaced_class_names.append(material_proxy.spaced_class_name)
        return material_proxy_spaced_class_names

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

    # TODO: change to boilerplate file stored in material_proxy package
    def make_material_proxy_class_file(self, material_proxy_name, generic_output_name):
        class_file_name = os.path.join(self.directory_name, material_proxy_name, material_proxy_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from abjad.tools import lilypondfiletools')
        lines.append('from baca.scf.materialproxies.MaterialProxy import MaterialProxy')
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

    def make_material_proxy_selection_menu(self):
        self.print_not_implemented()

    # TODO: change to boilerplate file stored in material_proxy package
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
        
    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_material_proxy()
        else:
            material_proxy_name = value
            material_proxy_name = material_proxy_name.replace(' ', '_')
            material_proxy_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(material_proxy_name)
            material_proxy = self.get_material_proxy(material_proxy_name)
            material_proxy.run()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_material_proxy_spaced_class_names()
        section = menu.make_new_section()
        section.append(('new', 'make material_proxy'))
        return menu

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
    def select_material_proxy_interactively(self, should_clear_terminal=True):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_material_proxy_spaced_class_names()
        while True:
            self.append_breadcrumb('select editor')
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
        material_proxy_name = result.replace(' ', '_')
        material_proxy_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(material_proxy_name)           
        material_proxy = self.get_material_proxy(material_proxy_name)
        return material_proxy

    def unimport_material_proxys_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)
