from baca.scf.SCFObject import SCFObject
from baca.scf.menuing.MenuObject import MenuObject
import os


class Menu(MenuObject, SCFObject):

    def __init__(self, client=None, menu_header=None, menu_body=None, 
        menu_sections=None, hidden_items=None, include_back=True, include_studio=True, 
        indent_level=1, item_width = 11, should_clear_terminal=True, hide_menu=False):
        MenuObject.__init__(
            self, menu_header=menu_header, menu_body=menu_body, hidden_items=hidden_items,
            indent_level=indent_level)
        self.client = client
        self.menu_sections = menu_sections
        self.include_back = include_back
        self.include_studio = include_studio
        self.item_width = item_width
        self.should_clear_terminal = should_clear_terminal
        self.hide_menu = hide_menu

    ### PUBLIC ATTRIBUTES ###
    
    @apply
    def hidden_items():
        def fget(self):
            return self._hidden_items
        def fset(self, hidden_items):
            if hidden_items is None:
                self._hidden_items = []
            else:
                self._hidden_items = hidden_items[:]
        return property(**locals())

    @apply
    def hide_menu():
        def fget(self):
            return self._hide_menu
        def fset(self, hide_menu):
            assert isinstance(hide_menu, type(True))
            self._hide_menu = hide_menu
        return property(**locals())

    @apply
    def include_back():
        def fget(self):
            return self._include_back
        def fset(self, include_back):
            assert isinstance(include_back, type(True))
            self._include_back = include_back
        return property(**locals())

    @apply
    def include_studio():
        def fget(self):
            return self._include_studio
        def fset(self, include_studio):
            assert isinstance(include_studio, type(True))
            self._include_studio = include_studio
        return property(**locals())

    @apply
    def item_width():
        def fget(self):
            return self._item_width
        def fset(self, item_width):
            assert isinstance(item_width, int)
            self._item_width = item_width
        return property(**locals())

    @apply
    def menu_sections():
        def fget(self):
            return self._menu_sections
        def fset(self, menu_sections):
            if menu_sections is None:
                self._menu_sections = []
            else:
                self._menu_sections = menu_sections[:]
        return property(**locals())

    @apply
    def should_clear_terminal():
        def fget(self):
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, type(True))
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    ### PUBLIC METHODS ###

    def add_hidden_menu_items(self, all_keys, all_values):
        for key, value in self.default_hidden_items:
            all_keys.append(key)
            all_values.append(value)
        for key, value in self.hidden_items:
            all_keys.append(key)
            all_values.append(value)
        
    def display(self, response=None, test=None):
        #print response, test, 'bar'
        if self.should_clear_terminal:
            if not response and test is None:
                self.clear_terminal()
        menu_lines, all_keys, all_values = self.make_menu_lines_keys_and_values()
        #if test == 'menu_lines' and not response:
        #    return menu_lines
        if not response and test == 'menu_lines':
            test_result = menu_lines
        else:
            test_result = None
        #print test_result, 'blah'
        self.add_hidden_menu_items(all_keys, all_values)
        if not response and not test:
            for menu_line in menu_lines:
                print menu_line
            while True:
                response = raw_input('scf> ')
                print ''
                if response in all_keys:
                    break
        if response:
            pair_dictionary = dict(zip(all_keys, all_values))
            value = pair_dictionary[response]
        else:
            value = None
        #return response, value
        return response, value, test_result

    def make_menu_lines_keys_and_values(self):
        menu_lines, all_keys, all_values = [], [], []
        menu_lines.extend(self.make_menu_title_lines())
        menu_lines.extend(self.make_menu_section_lines(all_keys, all_values))
        return menu_lines, all_keys, all_values

    def make_menu_lines(self):
        menu_lines, keys, values = self.make_menu_lines_keys_and_values()
        return menu_lines

    def make_menu_section_lines(self, all_keys, all_values):
        menu_lines = []
        for menu_section in self.menu_sections:
            menu_section.hide_menu = self.hide_menu
            menu_lines.extend(menu_section.make_menu_lines(all_keys, all_values))
        return menu_lines
        
    def make_menu_title_lines(self):
        menu_lines = []
        if self.menu_title:
            if not self.hide_menu:
                menu_title = self.menu_title.capitalize()
                menu_lines.append(menu_title)
                menu_lines.append('')
        return menu_lines

    def run(self, user_input=None, test=None):
        should_clear_terminal, hide_menu = True, False
        while True:
            response, user_input = self.split_user_input(user_input)
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            #print response, user_input, test, 'debug'
            key, value, test_result = self.display(response=response, test=test)
            #print 'menu.run', key, value, test_result, 'debug'
            should_clear_terminal, hide_menu = False, True
            result = self.handle_hidden_key(key, test=test)
            if result is True:
                pass
            elif bool(result):
                return None, None, user_input, result
            elif key == 'b':
                return key, None
            elif key == 'redraw':
                should_clear_terminal, hide_menu = True, False
            else:
                return key, value, user_input, test_result

    def split_user_input(self, user_input):
        if user_input:
            user_input = user_input.split('\n')
            response = user_input[0]
            user_input = '\n'.join(user_input[1:])
        else:
            response = None
        return response, user_input
