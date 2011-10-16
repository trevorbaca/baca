from abjad.tools import iotools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from baca.scf.PackageProxy import PackageProxy
from baca.scf.menuing import Menu
import os


class MakerWrangler(PackageProxy):

    def __init__(self):
        package_importable_name = 'baca.makers'
        PackageProxy.__init__(self, package_importable_name)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC METHODS ###

    def get_maker(self, maker_name):
        exec('from baca.makers import %s as maker_class' % maker_name)
        maker = maker_class()
        return maker

    def iterate_makers(self):
        self.unimport_baca_package()
        self.unimport_makers_package()
        exec('import baca')
        for maker_class_name in self.list_maker_class_names():
            exec('result = baca.makers.%s()' % maker_class_name)
            yield result

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

    def make_maker(self, menu_header=None):
        while True:
            maker_name = raw_input('Maker name> ')
            print ''
            if iotools.is_uppercamelcase_string(maker_name):
                if maker_name.endswith('Maker'):
                    break
        while True:
            generic_output_product = raw_input('Generic output product> ')
            print ''
            break
        maker_directory = os.path.join(self.directory_name, maker_name)
        os.mkdir(maker_directory)
        self.make_maker_initializer(maker_name)
        self.make_maker_class_file(maker_name, generic_output_product)
        self.make_maker_stylesheet(maker_name)

    def make_maker_initializer(self, maker_name):
        initializer_file_name = os.path.join(self.directory_name, maker_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools.importtools._import_structured_package import _import_structured_package\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("_import_structured_package(__path__[0], globals(), 'baca')\n")
        initializer.close() 

    def make_maker_class_file(self, maker_name, generic_output_name):
        class_file_name = os.path.join(self.directory_name, maker_name, maker_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from abjad.tools import lilypondfiletools')
        lines.append('from baca.scf._Maker import _Maker')
        lines.append('from baca.scf.UserInputWrapper import UserInputWrapper')
        lines.append('import os')
        lines.append('')
        lines.append('')
        lines.append('class %s(_Maker):' % maker_name)
        lines.append('')
        lines.append('\tdef __init__(self, **kwargs):')
        lines.append('\t\t_Maker.__init__(self, **kwargs)')
        lines.append("\t\tself.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')")
        lines.append("\t\tself._generic_output_name = %r" % generic_output_name)
        lines.append('')
        lines.append('\t### PUBLIC ATTRIBUTES ###')
        lines.append('')
        lines.append('\toutput_file_import_statements = [')
        lines.append('\t\t]')
        lines.append('')
        lines.append('\tuser_input_import_statements = [')
        lines.append('\t\t]')
        lines.append('')
        lines.append('\tuser_input_template = UserInputWrapper([')
        lines.append('\t\t])')
        lines.append('')
        lines.append('\t### PUBLIC METHODS ###')
        lines.append('')
        lines.append('\tdef get_output_file_lines(self, material, underscored_material_name):')
        lines.append('\t\toutput_file_lines = []')
        lines.append('\t\treturn output_file_lines')
        lines.append('')
        lines.append('\tdef make(self, foo, bar):')
        lines.append('\t\treturn material')
        lines.append('')
        lines.append('\tdef make_lilypond_file_from_output_material(self, material):')
        lines.append('\t\tlilypond_file = lilypondfiletools.make_basic_lilypond_file()')
        lines.append('\t\treturn lilypond_file')
        class_file.write('\n'.join(lines))
        class_file.close()

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
        
    def manage_makers(self, menu_header=None):
        while True:
            menu = Menu(client=self, menu_header=menu_header)
            menu.menu_body = 'select maker'
            menu.items_to_number = self.list_maker_spaced_class_names()
            menu.named_pairs.append(('new', 'make maker'))
            key, value = menu.display_menu()
            if key == 'b':
                return key, value
            elif key == 'new':
                self.make_maker(menu_header=menu_header)
            else:
                maker_name = value
                maker_name = maker_name.replace(' ', '_')
                maker_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(maker_name)
                maker = self.get_maker(maker_name)
                maker.manage_maker(menu_header=menu_header)

    def select_maker(self, menu_header=None):
        menu = Menu(client=self, menu_header=menu_header)
        menu.menu_body = 'select maker'
        menu.items_to_number = self.list_maker_spaced_class_names()
        key, value = menu.display_menu()
        if value is not None:
            maker_name = value.replace(' ', '_')
            maker_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(maker_name)           
            maker = self.get_maker(maker_name)
            return True, maker
        else:
            return True, None

    def unimport_makers_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)
