from abjad.tools import iotools
from abjad.tools import mathtools
from baca.scf.menuing.MenuObject import MenuObject
from baca.scf.menuing.MenuSection import MenuSection


class Menu(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._sections = []
        self.hide_menu = False

    ### PUBLIC ATTRIBUTES ###

    @property
    def argument_range_is_allowed(self):
        for section in self.sections:
            if section.allow_argument_range:
                return True
        return False
    
    @property
    def default_value(self):
        for section in self.sections:
            if section.has_default:
                return section.default_value

    @property
    def has_default(self):
        for section in self.sections:
            if section.has_default:
                return True
        return False

    @apply
    def hide_menu():
        def fget(self):
            return self._hide_menu
        def fset(self, hide_menu):
            assert isinstance(hide_menu, type(True))
            self._hide_menu = hide_menu
        return property(**locals())

    @property
    def sections(self):
        return self._sections

    ### PUBLIC METHODS ###

    def add_hidden_menu_items(self):
        for key, value in self.default_hidden_entries:
            self.all_keys.append(key)
            self.all_bodies.append(value)
        for key, value in self.hidden_entries:
            self.all_keys.append(key)
            self.all_bodies.append(value)

    def change_all_keys_to_lowercase(self):
        self.all_keys = [key.lower() for key in self.all_keys]

    def change_user_input_to_directive(self, user_input):
        if self.user_requests_default_value(user_input):
            return self.conditionally_enclose_in_list(self.default_value)
        elif not user_input:
            return
        elif user_input in self.all_keys:
            return user_input
        elif 'score'.startswith(user_input):
            return user_input
        elif 'studio'.startswith(user_input):
            return user_input
        elif self.user_requests_argument_range(user_input):
            return self.handle_argument_range_user_input(user_input)
        elif mathtools.is_integer_equivalent_expr(user_input):
            return self.handle_integer_user_input(user_input)
        else:
            return self.match_user_input_against_menu_entry_bodies(user_input)

    def handle_argument_range_user_input(self, user_input):
        for section in self.sections:
            if section.menu_values:
                break
        else:
            raise ValueError('no section contains numbered menu entries.')
        item_numbers = self.argument_range_string_to_numbers(user_input, section.menu_values)
        if item_numbers is None:
            return []
        item_indices = [item_number - 1 for item_number in item_numbers]
        for section in self.sections:
            if section.menu_values:
                result = []
                for i in item_indices:
                    item = section.menu_values[i]
                    result.append(item)
                return result

    def handle_integer_user_input(self, user_input):
        entry_number = int(user_input)
        for section in self.sections:
            if section.number_menu_entries:
                if entry_number <= len(section.menu_entry_tuples):
                    entry_index = entry_number - 1
                    key, body = section.menu_entry_tuples[entry_index]
                    if key:
                        value = key
                    else:
                        value = user_input
                    return self.conditionally_enclose_in_list(value)

    def strip_default_indicators_from_strings(self, expr):
        if isinstance(expr, list):
            cleaned_list = []
            for element in expr:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        elif expr is not None:
            if expr.endswith(' (default)'):
                expr = expr.replace(' (default)', '')
            return expr

    def conditionally_display_menu(self):
        self.conditionally_clear_terminal()
        self.make_menu_lines_keys_and_values()
        self.change_all_keys_to_lowercase()
        self.add_hidden_menu_items()
        self.conditionally_display_lines(self.menu_lines)
        user_response = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        user_input = self.split_multipart_user_response(user_response)
        user_input = iotools.strip_diacritics_from_binary_string(user_input)
        user_input = user_input.lower()
        directive = self.change_user_input_to_directive(user_input)
        directive = self.strip_default_indicators_from_strings(directive)
        self.session.hide_next_redraw = False
        directive = self.handle_hidden_key(directive)
        return directive

    def conditionally_enclose_in_list(self, expr):
        if self.argument_range_is_allowed:
            return [expr]
        else:
            return expr

    def make_menu_lines_keys_and_values(self):
        self.menu_lines, self.all_keys, self.all_bodies = [], [], []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_section_lines(self.all_keys, self.all_bodies))

    def make_menu_lines(self):
        menu_lines, keys, values = self.make_menu_lines_keys_and_values()
        return menu_lines

    def make_new_section(self):
        section = MenuSection(session=self.session, where=self.where)
        self.sections.append(section)
        return section

    def make_section_lines(self, all_keys, all_bodies):
        menu_lines = []
        for section in self.sections:
            menu_lines.extend(section.make_menu_lines(all_keys, all_bodies))
        if self.hide_menu:
            menu_lines = []
        return menu_lines
        
    def make_menu_title_lines(self):
        menu_lines = []
        if not self.hide_menu:
            menu_lines.append(iotools.capitalize_string_start(self.session.menu_header))
            menu_lines.append('')
        return menu_lines

    def match_user_input_against_menu_entry_bodies(self, user_input):
        for section in self.sections:
            for key, body in section.menu_entry_tuples:
                body = iotools.strip_diacritics_from_binary_string(body).lower()
                if body.startswith(user_input):
                    if key is not None:
                        value = key
                    else:
                        value = body
                    return self.conditionally_enclose_in_list(value)
                        
    def run(self, user_input=None):
        self.assign_user_input(user_input)
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            should_clear_terminal, hide_menu = False, True
            result = self.conditionally_display_menu()
            if self.session.is_complete:
                break
            elif result == 'redraw':
                should_clear_terminal, hide_menu = True, False
            else:
                break
        return result

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
                self.session.user_input = rest + ' ' + self.session.user_input
            else:
                self.session.user_input = rest
        else:
            key = user_response
        return key

    def user_requests_argument_range(self, user_input):
        if self.argument_range_is_allowed:
            if self.is_argument_range_string(user_input):
                return True
        return False

    def user_requests_default_value(self, user_input):
        if self.has_default:
            if user_input == '':
                return True
            elif 3 <= len(user_input) and 'default'.startswith(user_input):
                return True
        return False
