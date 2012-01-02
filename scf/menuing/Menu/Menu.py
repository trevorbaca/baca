from abjad.tools import iotools
from abjad.tools import mathtools
from baca.scf.menuing.MenuObject import MenuObject
from baca.scf.menuing.MenuSection import MenuSection


class Menu(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._sections = []
        self.sections.append(self.make_default_hidden_section(session=session, where=where))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def default_value(self):
        for section in self.sections:
            if section.has_default_value:
                return section.default_value

    @property
    def has_default_valued_section(self):
        for section in self.sections:
            if section.has_default_value:
                return True
        return False

    @property
    def has_hidden_section(self):
        for section in self.sections:
            if section.is_hidden:
                return True
        return False

    @property
    def has_keyed_section(self):
        for section in self.sections:
            if section.is_keyed:
                return True
        return False

    @property
    def has_numbered_section(self):
        for section in self.sections:
            if section.is_numbered:
                return True
        return False

    @property
    def has_ranged_section(self):
        for section in self.sections:
            if section.is_ranged:
                return True
        return False

    @property
    def menu_entry_bodies(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_bodies)
        return result

    @property
    def menu_entry_keys(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_keys)
        return result

    @property
    def menu_entry_return_values(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_return_values)
        return result

    @property
    def menu_entry_tokens(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_tokens)
        return result

    @property
    def numbered_section(self):
        for section in self.sections:
            if section.is_numbered:
                return section

    @property
    def ranged_section(self):
        for section in self.sections:
            if section.is_ranged:
                return section

    @property
    def sections(self):
        return self._sections

    @property
    def unpacked_menu_entries(self):
        result = []
        for section in self.sections:
            result.extend(section.unpacked_menu_entries)
        return result

    ### PUBLIC METHODS ###

    def change_user_input_to_directive(self, user_input):
        if self.user_enters_nothing(user_input):
            return self.handle_null_user_input(user_input)
        elif self.user_enters_backtracking_string(user_input):
            return self.conditionally_enclose_in_list(user_input)
        elif self.user_enters_menu_key(user_input):
            return self.handle_menu_key_user_input(user_input)
        elif self.user_enters_argument_range(user_input):
            return self.handle_argument_range_user_input(user_input)
        elif self.user_enters_integer_user_input(user_input):
            return self.handle_integer_user_input(user_input)
        elif self.user_enters_menu_body(user_input):
            return self.match_user_input_against_menu_entry_bodies(user_input)

    def change_menu_key_to_menu_body(self, menu_key):
        for number, key, body, return_value in self.unpacked_menu_entries:
            if key == menu_key:
                return body 

    def handle_argument_range_user_input(self, user_input):
        entry_numbers = self.ranged_section.argument_range_string_to_numbers(user_input)
        if entry_numbers is None:
            return []
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = self.ranged_section.menu_entry_return_values[i]
            result.append(entry)
        return result

    def handle_integer_user_input(self, user_input):
        entry_number = int(user_input)
        for section in self.sections:
            if section.is_numbered:
                if entry_number <= len(section.menu_entry_tokens):
                    entry_index = entry_number - 1
                    token = section.menu_entry_tokens[entry_index]
                    key, body = section.menu_entry_token_to_key_and_body(token)
                    if key:
                        value = key
                    else:
                        value = user_input
                    return self.conditionally_enclose_in_list(value)

    def handle_menu_key_user_input(self, menu_key):
        for number, key, body, return_value in self.unpacked_menu_entries:
            if key == menu_key:
                return self.conditionally_enclose_in_list(return_value)

    def handle_null_user_input(self, user_input):
        return self.conditionally_enclose_in_list(self.default_value)

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
        self.make_menu_lines()
        self.conditionally_display_lines(self.menu_lines)
        user_response = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        user_input = self.split_multipart_user_response(user_response)
        user_input = iotools.strip_diacritics_from_binary_string(user_input)
        user_input = user_input.lower()
        directive = self.change_user_input_to_directive(user_input)
        #print 'here: {!r}'.format(directive)
        directive = self.strip_default_indicators_from_strings(directive)
        self.session.hide_next_redraw = False
        directive = self.handle_hidden_key(directive)
        #print 'now: {!r}'.format(directive)
        return directive

    def conditionally_enclose_in_list(self, expr):
        if self.has_ranged_section:
            return [expr]
        else:
            return expr

    def make_menu_lines(self):
        self.menu_lines = []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_section_lines())

    def make_new_section(self, is_hidden=False, is_keyed=True, is_numbered=False, is_ranged=False):
        assert not (is_numbered and self.has_numbered_section)
        assert not (is_ranged and self.has_ranged_section)
        section = MenuSection(is_hidden=is_hidden, is_keyed=is_keyed, is_numbered=is_numbered,
            is_ranged=is_ranged, session=self.session, where=self.where)
        self.sections.append(section)
        return section

    def make_section_lines(self):
        menu_lines = []
        for section in self.sections:
            section_menu_lines = section.make_menu_lines()
            if not section.is_hidden:
                menu_lines.extend(section_menu_lines)
        if self._hide_current_run:
            menu_lines = []
        return menu_lines
        
    def make_menu_title_lines(self):
        menu_lines = []
        if not self._hide_current_run:
            menu_lines.append(iotools.capitalize_string_start(self.session.menu_header))
            menu_lines.append('')
        return menu_lines

    def match_user_input_against_menu_entry_bodies(self, user_input):
        for section in self.sections:
            for token in section.menu_entry_tokens:
                key, body = section.menu_entry_token_to_key_and_body(token)
                body = iotools.strip_diacritics_from_binary_string(body).lower()
                if body.startswith(user_input):
                    if key is not None:
                        value = key
                    else:
                        value = body
                    return self.conditionally_enclose_in_list(value)

    def user_enters_menu_body(self, user_input):
        for number, key, body, return_value in self.unpacked_menu_entries:
            body = iotools.strip_diacritics_from_binary_string(body).lower()
            if body.startswith(user_input):
                return True
        return False
                        
    # TODO: globally remove should_clear_terminal
    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        should_clear_terminal, hide_current_run = True, False
        while True:
            self._should_clear_terminal, self._hide_current_run = should_clear_terminal, hide_current_run
            should_clear_terminal, hide_current_run = False, True
            result = self.conditionally_display_menu()
            if self.session.is_complete:
                break
            elif result == 'redraw':
                should_clear_terminal, hide_current_run = True, False
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
            if isinstance(self.session.user_input, str) and rest:
                self.session.user_input = rest + ' ' + self.session.user_input
            else:
                self.session.user_input = rest
        else:
            key = user_response
        return key

    def user_enters_argument_range(self, user_input):
        if self.has_ranged_section:
            if self.is_argument_range_string(user_input):
                return True
        return False

    def user_enters_backtracking_string(self, user_input):
        if isinstance(user_input, str) and 3 <= len(user_input):
            if 'studio'.startswith(user_input):
                return True
            elif 'score'.startswith(user_input):
                return True
        return False
    
    def user_enters_integer_user_input(self, user_input):
        return mathtools.is_integer_equivalent_expr(user_input)

    def user_enters_menu_key(self, user_input):
        return user_input in self.menu_entry_keys

    def user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and 'default'.startswith(user_input))
