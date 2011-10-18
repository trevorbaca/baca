from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
from baca.scf.menuing.MenuObject import MenuObject
import os


class Menu(MenuObject, SCFObject):

    def __init__(self, hidden_items=None, hide_menu=False, include_back=True, 
        include_studio=True, indent_level=1, item_width=11, sections=None, 
        session=None, should_clear_terminal=True, where=None):
        MenuObject.__init__(self, hidden_items=hidden_items, indent_level=indent_level, 
            session=session, should_clear_terminal=should_clear_terminal)
        self.hide_menu = hide_menu
        self.include_back = include_back
        self.include_studio = include_studio
        self.item_width = item_width
        self.sections = sections
        self.where = where

    ### PUBLIC ATTRIBUTES ###
    
    @property
    def has_default(self):
        for section in self.sections:
            if section.has_default:
                return True
        return False

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
    def sections():
        def fget(self):
            return self._sections
        def fset(self, sections):
            if sections is None:
                self._sections = []
            else:
                self._sections = sections[:]
        return property(**locals())

    ### PUBLIC METHODS ###

    def add_hidden_menu_items(self):
        for key, value in self.default_hidden_items:
            self.all_keys.append(key)
            self.all_values.append(value)
        for key, value in self.hidden_items:
            self.all_keys.append(key)
            self.all_values.append(value)

    def change_key_to_value(self, key):
        if key:
            pair_dictionary = dict(zip(self.all_keys, self.all_values))
            return pair_dictionary.get(key)

    def change_value_to_key(self, value):
        if value:
            pair_dictionary = dict(zip(self.all_values, self.all_keys))
            return pair_dictionary.get(value)

    def check_if_key_exists(self, key):
        if self.key_is_default(key):
            value = self.get_default_value()
            return self.change_value_to_key(value)
        elif key in self.all_keys:
            return key
        else:
            return self.check_for_matching_value_string(key)

    def check_for_matching_value_string(self, key):
        for value in self.all_values:
            if value.startswith(key):
                key = self.change_value_to_key(value)
                return key 

    def clean_value(self, value):
        if value is not None:
            if value.endswith(' (default)'):
                value = value.replace(' (default)', '')
            return value

    def conditionally_display_menu(self):
        if not self.session.hide_next_redraw:
            self.conditionally_clear_terminal()
        self.make_menu_lines_keys_and_values()
        self.add_hidden_menu_items()
        if not self.session.hide_next_redraw:
            self.display_lines(self.menu_lines)
        key = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        key = self.check_if_key_exists(key)
        value = self.change_key_to_value(key)
        value = self.clean_value(value)
        self.session.hide_next_redraw = False
        return key, value

    def get_default_value(self):
        for section in self.sections:
            if section.has_default:
                return section.get_default_value() 

    def key_is_default(self, key):
        if 3 <= len(key):
            if 'default'.startswith(key):
                return True
        return False

    def make_menu_lines_keys_and_values(self):
        self.menu_lines, self.all_keys, self.all_values = [], [], []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_section_lines(self.all_keys, self.all_values))

    def make_menu_lines(self):
        menu_lines, keys, values = self.make_menu_lines_keys_and_values()
        return menu_lines

    def make_section_lines(self, all_keys, all_values):
        menu_lines = []
        for section in self.sections:
            section.hide_menu = self.hide_menu
            menu_lines.extend(section.make_menu_lines(all_keys, all_values))
        return menu_lines
        
    def make_menu_title_lines(self):
        menu_lines = []
        if not self.hide_menu:
            menu_lines.append(iotools.capitalize_string_start(self.session.menu_header))
            menu_lines.append('')
        return menu_lines

    @apply
    def prompt_default():
        def fget(self): 
            if self.has_default:
                return 'def'
            return self._prompt_default
        def fset(self, prompt_default):
            assert isinstance(prompt_default, (str, type(None)))
            self._prompt_default = prompt_default
        return property(**locals())

    def run(self):
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            key, value = self.conditionally_display_menu()
            should_clear_terminal, hide_menu = False, True
            key = self.handle_hidden_key(key)
            if self.session.is_complete:
                break
            elif key == 'redraw':
                should_clear_terminal, hide_menu = True, False
            else:
                break
        return key, value
