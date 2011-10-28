from baca.scf.menuing._MenuObject import _MenuObject
from baca.scf._SCFObject import _SCFObject
import os


class Menu(_MenuObject, _SCFObject):

    def __init__(self, client=None, menu_header=None, menu_body=None, 
        menu_sections=None, hidden_items=None, include_back=True, include_studio=True, 
        indent_level=1, item_width = 11, should_clear_terminal=True, hide_menu=False):
        _MenuObject.__init__(
            self, menu_header=menu_header, menu_body=menu_body, hidden_items=hidden_items,
            indent_level=indent_level)
        self.client = client
        self.menu_sections = menu_sections
        self.include_back = include_back
        self.include_studio = include_studio
        self.item_width = item_width
        self.should_clear_terminal = should_clear_terminal
        self.hide_menu = hide_menu

    ### PRIVATE METHODS ###

    def _add_hidden_menu_items(self, all_keys, all_values):
        for key, value in self.default_hidden_items:
            all_keys.append(key)
            all_values.append(value)
        for key, value in self.hidden_items:
            all_keys.append(key)
            all_values.append(value)
        
    def _display_menu(self):
        if self.should_clear_terminal:
            self.clear_terminal()
        all_keys, all_values = [], []
        self._display_menu_title()
        self._display_menu_sections(all_keys, all_values)
        self._add_hidden_menu_items(all_keys, all_values)
        while True:
            response = raw_input('scf> ')
            print ''
            if response in all_keys:
                break
        pair_dictionary = dict(zip(all_keys, all_values))
        value = pair_dictionary[response]
        return response, value

    def _display_menu_sections(self, all_keys, all_values):
        for menu_section in self.menu_sections:
            menu_section.hide_menu = self.hide_menu
            menu_section.display(all_keys, all_values)
        
    def _display_menu_title(self):
        if self.menu_title:
            if not self.hide_menu:
                menu_title = self.menu_title.capitalize()
                print menu_title
                print ''

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

    def display_menu(self):
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            key, value = self._display_menu()
            should_clear_terminal, hide_menu = False, True
            if self.handle_hidden_key(key):
                pass
            elif key == 'b':
                return key, None
            elif key == 'redraw':
                should_clear_terminal, hide_menu = True, False
            else:
                return key, value
