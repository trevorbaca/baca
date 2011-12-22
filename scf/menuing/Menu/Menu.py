from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
from baca.scf.menuing.MenuObject import MenuObject
from baca.scf.menuing.MenuSection import MenuSection
import os


class Menu(MenuObject, SCFObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self.allow_argument_range = False
        self.hide_menu = False
        self.sections = None

    ### PUBLIC ATTRIBUTES ###

    @apply
    def allow_argument_range():
        def fget(self):
            return self._allow_argument_range
        def fset(self, allow_argument_range):
            assert isinstance(allow_argument_range, type(True))
            self._allow_argument_range = allow_argument_range
        return property(**locals())
    
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
    def prompt_default():
        def fget(self):
            return self._prompt_default
        def fset(self, prompt_default):
            assert isinstance(prompt_default, (str, type(None)))
            self._prompt_default = prompt_default
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
            self.all_display_strings.append(None)
        for key, value in self.hidden_items:
            self.all_keys.append(key)
            self.all_values.append(value)
            self.all_display_strings.append(None)

    def change_all_keys_to_lowercase(self):
        self.all_keys = [key.lower() for key in self.all_keys]

    def change_display_string_to_key(self, display_string):
        if display_string:
            pair_dictionary = dict(zip(self.all_display_strings, self.all_keys))
            return pair_dictionary.get(display_string)

    def change_key_to_value(self, key):
        from abjad.tools import sequencetools
        if key:
            pair_dictionary = dict(zip(self.all_keys, self.all_values))
            if key in pair_dictionary:
                value = pair_dictionary.get(key)
                if self.allow_argument_range:
                    return [value]
                else:
                    return value
            elif self.allow_argument_range and self.is_argument_range_string(key):
                for section in self.sections:
                    if section.items_to_number:
                        break
                else:
                    raise ValueError('no section contains items to number.')
                item_numbers = self.argument_range_string_to_numbers(key, section.items_to_number)
                if item_numbers is None:
                    return []
                item_indices = [item_number - 1 for item_number in item_numbers]
                for section in self.sections:
                    if section.items_to_number:
                        result = []
                        for i in item_indices:
                            item = section.items_to_number[i]
                            result.append(item)
                        return result

    def change_value_to_key(self, value):
        if value:
            pair_dictionary = dict(zip(self.all_values, self.all_keys))
            return pair_dictionary.get(value)

    def check_if_key_exists(self, key):
        if self.key_is_default(key):
            value = self.get_default_value()
            return self.change_value_to_key(value)
        elif key == '' and self.has_default:
            value = self.get_default_value()
            return self.change_value_to_key(value)
        elif key in self.all_keys:
            return key
        elif isinstance(key, str) and 3 <= len(key) and 'score'.startswith(key):
            return key
        elif isinstance(key, str) and 3 <= len(key) and 'studio'.startswith(key):
            return key
        elif self.allow_argument_range and self.is_argument_range_string(key):
            for section in self.sections:
                if section.items_to_number:
                    break
            else:
                raise ValueError('no section contains items to number.')
            if self.is_valid_argument_range_string_for_argument_list(key, section.items_to_number):
                return key
            else:
                return None
        else:
            return self.check_for_matching_value_string(key)

    def check_for_matching_value_string(self, key):
        if key:
            assert len(self.all_values) == len(self.all_display_strings)
            for value, display_string in zip(self.all_values, self.all_display_strings):
                if 3 <= len(key) and iotools.strip_diacritics_from_binary_string(value).lower().startswith(key):
                    key = self.change_value_to_key(value)
                    return key
                elif display_string is not None and iotools.strip_diacritics_from_binary_string(
                    display_string).lower().startswith(key):
                    key = self.change_display_string_to_key(display_string)
                    return key 

    def clean_value(self, value):
        if isinstance(value, list):
            cleaned_list = []
            for element in value:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        elif value is not None:
            if value.endswith(' (default)'):
                value = value.replace(' (default)', '')
            return value

    def conditionally_display_menu(self):
        if not self.session.hide_next_redraw:
            self.conditionally_clear_terminal()
        self.make_menu_lines_keys_and_values()
        self.change_all_keys_to_lowercase()
        self.add_hidden_menu_items()
        if not self.session.hide_next_redraw:
            self.display_lines(self.menu_lines)
        user_response = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        key = self.split_multipart_user_response(user_response)
        key = iotools.strip_diacritics_from_binary_string(key)
        key = key.lower()
        #print 'BAR', repr(user_response), repr(key), '||', repr(self.session.user_input)
        key = self.check_if_key_exists(key)
        #print 'exists?', repr(key)
        value = self.change_key_to_value(key)
        #print repr(value)
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
        self.menu_lines, self.all_keys, self.all_values, self.all_display_strings = [], [], [], []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_section_lines(
            self.all_keys, self.all_values, self.all_display_strings))

    def make_menu_lines(self):
        menu_lines, keys, values = self.make_menu_lines_keys_and_values()
        return menu_lines

    def make_new_section(self):
        section = MenuSection(session=self.session, where=self.where)
        self.sections.append(section)
        return section

    def make_section_lines(self, all_keys, all_values, all_display_strings):
        menu_lines = []
        for section in self.sections:
            menu_lines.extend(section.make_menu_lines(all_keys, all_values, all_display_strings))
        if self.hide_menu:
            menu_lines = []
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

    def split_multipart_user_response(self, user_response):
        self.session.transcribe_next_command = True
        if ' ' in user_response:
            parts = user_response.split(' ')
            key_parts, rest_parts = [], []
            for i, part in enumerate(parts):
                if not part.endswith((',', '-')):
                    break
            key_parts = parts[:i+1]
            rest_parts = parts[i+1:]
            key = ' '.join(key_parts)
            rest = ' '.join(rest_parts)
            if rest:
                self.session.transcribe_next_command = False
            if isinstance(self.session.user_input, str):
                #self.session.user_input = self.session.user_input + ' ' + rest
                self.session.user_input = rest + ' ' + self.session.user_input
            else:
                self.session.user_input = rest
        else:
            key = user_response
        return key
