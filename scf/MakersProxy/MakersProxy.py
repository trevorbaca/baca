from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.DirectoryProxy import DirectoryProxy
import os


class MakersProxy(DirectoryProxy):

    def __init__(self):
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

    def manage_makers(self):
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_title = 'Interactive Material Makers'
            menu_specifier.items_to_number = self.list_makers()
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, value
            elif key == 'S':
                return 'studio'
            else:
                maker_name = value
                maker = self.get_maker(maker_name)
                maker.make_interactively()

    def select_interactive_maker(self, score_title=None):
        menu_specifier = MenuSpecifier()
        menu_specifier.menu_title = 'Select interactive material maker'
        menu_specifier.items_to_number = self.list_makers()
        key, value = menu_specifier.display_menu(score_title=score_title)
        if value is not None:
            maker_name = value
            maker = self.get_maker(maker_name)
            return maker
        else:
            return None
