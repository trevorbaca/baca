from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
from baca.scf.menuing.MenuObject import MenuObject
import os


class Menu(MenuObject, SCFObject):

    def __init__(self, hide_menu=False, menu_sections=None, hidden_items=None, include_back=True, 
        include_studio=True, indent_level=1, item_width=11, session=None, should_clear_terminal=True, 
        where=None):
        MenuObject.__init__(self, hidden_items=hidden_items, indent_level=indent_level, 
            session=session, should_clear_terminal=should_clear_terminal)
        self.hide_menu = hide_menu
        self.include_back = include_back
        self.include_studio = include_studio
        self.item_width = item_width
        self.menu_sections = menu_sections
        self.where = where

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

    ### PUBLIC METHODS ###

    def add_hidden_menu_items(self):
        for key, value in self.default_hidden_items:
            self.all_keys.append(key)
            self.all_values.append(value)
        for key, value in self.hidden_items:
            self.all_keys.append(key)
            self.all_values.append(value)

    def change_user_response_to_value(self, user_response):
        if user_response:
            pair_dictionary = dict(zip(self.all_keys, self.all_values))
            return pair_dictionary[user_response]

    def conditionally_display_menu_lines_and_get_user_response(self):
        if self.session.is_displayable:
            for menu_line in self.menu_lines:
                print menu_line
            while True:
                user_response = raw_input('scf> ')
                print ''
                if user_response in self.all_keys:
                    return user_response
        else:
            user_response = self.pop_next_user_response_from_user_input()
            if user_response == '':
                user_response = None
            if user_response is None:
                if self.session.test == 'menu_lines':
                    self.session.test_result = self.menu_lines
            return user_response

    def display(self):
        self.conditionally_clear_terminal()
        self.make_menu_lines_keys_and_values()
        self.add_hidden_menu_items()
        user_response = self.conditionally_display_menu_lines_and_get_user_response()
        value = self.change_user_response_to_value(user_response)
        return user_response, value

    def make_menu_lines_keys_and_values(self):
        self.menu_lines, self.all_keys, self.all_values = [], [], []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_menu_section_lines(self.all_keys, self.all_values))

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
        if not self.hide_menu:
            menu_lines.append(iotools.capitalize_string_start(self.session.menu_header))
            menu_lines.append('')
        return menu_lines

    def run(self):
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            key, value = self.display()
            should_clear_terminal, hide_menu = False, True
            result = self.handle_hidden_key(key)
            if result is True:
                pass
            elif bool(result):
                self.session.test_result = result
                key, value = None, None
                break
            elif key == 'b':
                value = None
                break
            elif key == 'redraw':
                should_clear_terminal, hide_menu = True, False
            else:
                break
        return key, value
