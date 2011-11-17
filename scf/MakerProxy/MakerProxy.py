from abjad.tools import iotools
from baca.scf.PackageProxy import PackageProxy
import os


class MakerProxy(PackageProxy):

    def __init__(self, maker_class_name=None, session=None):
        self.maker_class_name = maker_class_name
        if maker_class_name is not None:
            package_importable_name = 'baca.makers.%s' % maker_class_name
        else:
            package_importable_name = None
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)

    ### OVERLOADS ###

    def __repr__(self):
        if self.maker_class_name is None:
            return '{}()'.format(self.class_name)
        else:
            return '{}({!r})'.format(self.class_name, self.maker_class_name)

    ### PUBLIC ATTRIBUTES ###

    # TODO: Maybe this can't be set here? Must be derived from hardcode maker classfile?
    @apply
    def generic_output_name():
        def fget(self):
            return self._generic_output_name
        def fset(self, generic_output_name):
            assert isinstance(generic_output_name, (str, type(None)))
            if isinstance(generic_output_name):
                assert iotools.is_underscore_delimited_lowercase_string(generic_output_name)
            self._generic_output_name = generic_output_name
        return property(**locals())

    @apply
    def maker_class_name():
        def fget(self):
            return self._maker_class_name
        def fset(self, maker_class_name):
            assert isinstance(maker_class_name, (str, type(None)))
            if isinstance(maker_class_name, str):
                assert iotools.is_uppercamelcase_string(maker_class_name)
            self._maker_class_name = maker_class_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def add_line_to_initializer(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    # TODO: Possibly MakerWrangler?
    def add_line_to_materials_initializer(self):
        material_underscored_name = os.path.basename(self.material_package_directory)
        import_statement = 'from %s import %s\n' % (material_underscored_name, material_underscored_name)
        initializer = self._get_initializer()
        self._add_line_to_initializer(initializer, import_statement)

    def get_initializer(self):
        if 'scores' in self.material_package_directory:
            materials_directory = os.path.dirname(self.material_package_directory)
            initializer = os.path.join(materials_directory, '__init__.py')
        else:
            initializer = os.path.join(os.environ.get('BACA'), 'materials', '__init__.py')        
        return initializer

    def manage_maker(self, menu_header=None):
        while True:
            menu = self.Menu(where=self.where(), session=self.session)
            menu.menu_header = menu_header
            menu.menu_body = self.spaced_class_name
            menu_section = self.MenuSection()
            menu_section.menu_section_title = 'existing %s' % self.generic_output_name
            menu_section.items_to_number = list(self.iterate_materials_based_on_maker())
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.sentence_length_items.append(('del', 'delete %s' % self.spaced_class_name))
            menu_section.sentence_length_items.append(('new', 'create %s' % self.generic_output_name))
            menu_section.sentence_length_items.append(('ren', 'rename %s' % self.spaced_class_name))
            menu_section.sentence_length_items.append(('src', 'edit %s source' % self.spaced_class_name))
            key, value = menu.run()
            if key == 'b':
                return key, None
            elif key == 'del':
                self.delete_package()
                break
            elif key == 'new':
                self.edit_interactively(menu_header=menu.menu_title)
            elif key == 'ren':
                self.print_not_implemented()
            elif key == 'src':
                self.edit_source_file()
            else:
                material_proxy = value
                material_proxy.manage_material(menu_header=menu.menu_title)

    def write_initializer_to_disk(self):
        initializer = file(os.path.join(self.material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.write('import datetime\n')
        initializer.write('\n\n')
        tags_dictionary = self.make_tags_dictionary()
        initializer.write('tags = %r\n' % tags_dictionary)
        initializer.close()
