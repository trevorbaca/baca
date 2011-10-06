from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.MenuSpecifier import MenuSpecifier
import os


class MakersProxy(DirectoryProxy):

    def __init__(self, score_title=None):
        self.score_title = score_title
        self.makers_directory = os.path.join(os.environ.get('BACA'), 'makers')

    ### PUBLIC METHODS ###

    def get_maker(self, maker_name):
        exec('from baca.makers import %s as maker_class' % maker_name)
        maker = maker_class()
        return maker

    def list_makers(self):
        maker_directories = []
        for name in os.listdir(self.makers_directory):
            if name[0].isalpha():
                directory = os.path.join(self.makers_directory, name)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        maker_directories.append(name)
        return maker_directories

    def list_maker_class_spaced_names(self):
        class_spaced_names = []
        for maker in self.list_makers():
            class_spaced_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(maker)
            class_spaced_name = class_spaced_name.replace('_', ' ')
            class_spaced_names.append(class_spaced_name)
        return class_spaced_names

    def manage_makers(self, menu_header=None):
        while True:
            menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier.menu_body = 'interactive material makers'
            menu_specifier.items_to_number = self.list_maker_class_spaced_names()
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, value
            else:
                maker_name = value
                maker_name = maker_name.replace(' ', '_')
                maker_name = iotools.underscore_delimited_lowercase_to_uppercamelcase(maker_name)
                maker = self.get_maker(maker_name)
                menu_header = ' - '.join(menu_specifier.menu_title_parts[:-2])
                result = maker.edit_interactively(menu_header=menu_header)
                if result:
                    break

    def select_interactive_maker(self, menu_header=None):
        menu_specifier = MenuSpecifier(menu_header=menu_header)
        menu_specifier.menu_body = 'select interactive material maker'
        menu_specifier.items_to_number = self.list_makers()
        key, value = menu_specifier.display_menu()
        if value is not None:
            maker_name = value
            maker = self.get_maker(maker_name)
            return True, maker
        else:
            return True, None
