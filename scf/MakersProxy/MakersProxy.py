from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.SCFProxyObject import SCFProxyObject
import os


class MakersProxy(SCFProxyObject):

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

    def select_interactive_maker(self, show_menu_title=True):
        is_first_pass = True
        while True:
            is_redraw = False
            menu_specifier = MenuSpecifier()
            if show_menu_title:
                menu_specifier.menu_title = 'Select interactive material maker'
            menu_specifier.items_to_number = self.list_makers()
            key, value = menu_specifier.display_menu(clear_terminal=False)
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
                return maker
                #is_redraw = True
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False
