from abjad.tools import iotools
from abjad.tools import mathtools
from baca.scf.menuing.MenuObject import MenuObject
from baca.scf.menuing.MenuSection import MenuSection


class Menu(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._sections = []
        # TODO: allow self.use_menu_entry_key_as_menu_entry_return_value on MenuSection only
        self.use_menu_entry_key_as_menu_entry_return_value = True
        default_hidden_section = self.make_default_hidden_section(session=session, where=where)
        self.sections.append(default_hidden_section)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def argument_range_is_allowed(self):
        for section in self.sections:
            if section.allow_argument_range:
                return True
        return False
    
    @property
    def default_value(self):
        for section in self.sections:
            if section.has_default_value:
                return section.default_value

    @property
    def has_default_value(self):
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
    def numbered_section(self):
        for section in self.sections:
            if section.is_numbered:
                return section

    @property
    def sections(self):
        return self._sections

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def use_menu_entry_key_as_menu_entry_return_value():
        def fget(self):
            return self._use_menu_entry_key_as_menu_entry_return_value
        def fset(self, use_menu_entry_key_as_menu_entry_return_value):
            assert isinstance(use_menu_entry_key_as_menu_entry_return_value, type(True))
            self._use_menu_entry_key_as_menu_entry_return_value = use_menu_entry_key_as_menu_entry_return_value
        return property(**locals())

    ### PUBLIC METHODS ###

    def add_hidden_menu_items(self):
        for key, value in self.default_hidden_entries:
            self.all_keys.append(key)
            self.all_bodies.append(value)
        for key, value in self.hidden_entries:
            self.all_keys.append(key)
            self.all_bodies.append(value)

    def change_all_keys_to_lowercase(self):
        all_keys = []
        for key in self.all_keys:
            if key is None:
                all_keys.append(key)
            elif isinstance(key, str):
                all_keys.append(key.lower())
            else:
                raise TypeError

    def change_user_input_to_directive(self, user_input):
        if self.user_requests_default_value(user_input):
            return self.conditionally_enclose_in_list(self.default_value)
        elif not user_input:
            return
        elif user_input in self.all_keys:
            return self.handle_menu_key_user_input(user_input)
        elif 'score'.startswith(user_input):
            return user_input
        elif 'studio'.startswith(user_input):
            print 'ZZZ'
            return user_input
        elif self.user_requests_argument_range(user_input):
            return self.handle_argument_range_user_input(user_input)
        elif mathtools.is_integer_equivalent_expr(user_input):
            return self.handle_integer_user_input(user_input)
        else:
            return self.match_user_input_against_menu_entry_bodies(user_input)

    def change_menu_key_to_menu_body(self, menu_key):
        return dict(zip(self.all_keys, self.all_bodies)).get(menu_key)

    # TODO: rename 'opt' as 'menu_keys' ... or just pass section.menu_entry_tokens
    def handle_argument_range_user_input(self, user_input):
        numbered_section = self.numbered_section
        assert numbered_section is not None
        item_numbers = self.argument_range_string_to_numbers(user_input, 
            numbered_section.menu_entry_return_values, opt=numbered_section.menu_entry_keys)
        if item_numbers is None:
            return []
        item_indices = [item_number - 1 for item_number in item_numbers]
        result = []
        for i in item_indices:
            item = numbered_section.menu_entry_return_values[i]
            result.append(item)
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

    def handle_menu_key_user_input(self, user_input):
        if self.use_menu_entry_key_as_menu_entry_return_value:
            directive = user_input
        else:
            directive = self.change_menu_key_to_menu_body(user_input)
        return self.conditionally_enclose_in_list(directive)

    def is_backtracking_string(self, expr):
        if isinstance(expr, str) and 3 <= len(expr):
            if 'studio'.startswith(expr):
                return True
            elif 'score'.startswith(expr):
                return True
        return False

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
        #print 'here: {!r}'.format(directive)
        directive = self.strip_default_indicators_from_strings(directive)
        self.session.hide_next_redraw = False
        directive = self.handle_hidden_key(directive)
        #print 'now: {!r}'.format(directive)
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

    def make_new_section(self, is_hidden=False, is_keyed=True, is_numbered=False):
        assert not (is_numbered and self.has_numbered_section)
        section = MenuSection(is_hidden=is_hidden, is_keyed=is_keyed, is_numbered=is_numbered,
            session=self.session, where=self.where)
        self.sections.append(section)
        return section

    def make_section_lines(self, all_keys, all_bodies):
        menu_lines = []
        for section in self.sections:
            section_menu_lines = section.make_menu_lines(all_keys, all_bodies)
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

    def user_requests_argument_range(self, user_input):
        if self.argument_range_is_allowed:
            if self.is_argument_range_string(user_input):
                return True
        return False

    def user_requests_default_value(self, user_input):
        if self.has_default_value:
            if user_input == '':
                return True
            elif 3 <= len(user_input) and 'default'.startswith(user_input):
                return True
        return False
