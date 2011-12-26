from abjad.tools import iotools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from baca.scf.PackageProxy import PackageProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


# TODO: implement MakerProxy and implement MakerWrangler in terms of MakerProxy
class MakerWrangler(PackageWrangler, PackageProxy):

    def __init__(self, session=None):
        package_importable_name = 'baca.makers'
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        PackageWrangler.__init__(self, directory_name=self.directory_name, session=self.session)

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### PUBIC ATTRIBUTES ###

    def Maker(self):
        import baca
        return baca.scf.Maker

    ### PUBLIC METHODS ###

    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    def get_maker(self, maker_name):
        exec('from baca.makers import {} as maker_class'.format(maker_name))
        maker = maker_class()
        return maker

    def get_package_proxy(self, package_importable_name):
        return self.Maker(package_importable_name)

    # replace with wrapped call to PackageWrangler.iterate_package_proxies()
    def iterate_makers(self):
        self.unimport_baca_package()
        self.unimport_makers_package()
        exec('import baca')
        for maker_class_name in self.list_maker_class_names():
            exec('result = baca.makers.{}()'.format(maker_class_name))
            yield result

    # add PackageWrangler.iterate_package_class_names and replace this with it
    def list_maker_class_names(self):
        maker_directories = []
        for name in os.listdir(self.directory_name):
            if name[0].isalpha():
                directory = os.path.join(self.directory_name, name)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        maker_directories.append(name)
        return maker_directories

    def list_maker_spaced_class_names(self):
        maker_spaced_class_names = []
        for maker in self.iterate_makers():
            maker_spaced_class_names.append(maker.spaced_class_name)
        return maker_spaced_class_names

    # replace with maker wizard
    def make_maker(self):
        while True:
            maker_name = self.handle_raw_input('maker name')
            if iotools.is_uppercamelcase_string(maker_name):
                if maker_name.endswith('Maker'):
                    break
        while True:
            generic_output_product = self.handle_raw_input('generic output product')
            break
        maker_directory = os.path.join(self.directory_name, maker_name)
        os.mkdir(maker_directory)
        self.make_maker_initializer(maker_name)
        self.make_maker_class_file(maker_name, generic_output_product)
        self.make_maker_stylesheet(maker_name)

    # TODO: change to boilerplate file stored in maker package
    def make_maker_initializer(self, maker_name):
        initializer_file_name = os.path.join(self.directory_name, maker_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools.importtools._import_structured_package import _import_structured_package\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("_import_structured_package(__path__[0], globals(), 'baca')\n")
        initializer.close() 

    # TODO: change to boilerplate file stored in maker package
    def make_maker_class_file(self, maker_name, generic_output_name):
        class_file_name = os.path.join(self.directory_name, maker_name, maker_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from abjad.tools import lilypondfiletools')
        lines.append('from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy')
        lines.append('from baca.scf.UserInputWrapper import UserInputWrapper')
        lines.append('import os')
        lines.append('')
        lines.append('')
        lines.append('class {}(InteractiveMaterialProxy):'.format(maker_name))
        lines.append('')
        lines.append('    def __init__(self, **kwargs):')
        lines.append('        Maker.__init__(self, **kwargs)')
        lines.append("        self.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')")
        lines.append("        self._generic_output_name = {!r}".format(generic_output_name))
        lines.append('')
        lines.append('    ### PUBLIC ATTRIBUTES ###')
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

    # TODO: change to boilerplate file stored in maker package
    def make_maker_stylesheet(self, maker_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.makup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(self.directory_name, maker_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()
        
    def handle_main_menu_result(self, result):
        if result == 'b':
            return 'back'
        elif result == 'new':
            self.make_maker()
        else:
            maker_name = value
            maker_name = maker_name.replace(' ', '_')
            maker_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(maker_name)
            maker = self.get_maker(maker_name)
            maker.run()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tuples = [('', x) for x in self.list_maker_spaced_class_names()]
        section.number_menu_entries = True
        section = menu.make_new_section()
        section.menu_entry_tuples.append(('new', 'make maker'))
        return menu

    def run(self, user_input=None):
        self.assign_user_input(user_input)
        while True:
            self.breadcrumbs.append('makers')
            menu = self.make_main_menu()
            result = menu.run()
            if self.backtrack():
                break
            elif not result:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.breadcrumbs.pop()
        self.breadcrumbs.pop()

    def select_maker(self):
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tuples = [('', x) for x in self.list_maker_spaced_class_names()]
        section.number_menu_entries = True
        result = menu.run()
        if result is not None:
            maker_name = result.replace(' ', '_')
            maker_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(maker_name)           
            maker = self.get_maker(maker_name)
            return True, maker
        else:
            return True, None

    def unimport_makers_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)
