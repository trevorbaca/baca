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
        is_first_pass = True
        while True:
            is_redraw = False
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_title = 'Interactive material makers'
            menu_specifier.items_to_number = self.list_makers()
            key, value = menu_specifier.display_menu()
            result = None
            if key == 'b':
                return 'b'
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                is_redraw = True
            elif key == 'x':
                self.exec_statement()
            else:
                maker_name = value
                maker = self.get_maker(maker_name)
                maker.make_interactively()
                is_redraw = True
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False

    def select_interactive_maker(self, score_title=None, show_menu_title=True):
        clear_terminal, hide_menu = True, False
        while True:
            menu_specifier = MenuSpecifier()
            if show_menu_title:
                menu_title = 'Select interactive material maker'
                if score_title is not None:
                    menu_title = '%s - %s' % (score_title, menu_title.lower())
                menu_specifier.menu_title = menu_title
            menu_specifier.items_to_number = self.list_makers()
            menu_specifier.clear_terminal, menu_specifier.hide_menu = clear_terminal, hide_menu
            key, value = menu_specifier.display_menu()
            clear_terminal, hide_menu = False, True
            if key == 'b':
                return None
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                clear_terminal, hide_menu = True, False
            elif key == 'x':
                self.exec_statement()
            else:
                maker_name = value
                maker = self.get_maker(maker_name)
                return maker
