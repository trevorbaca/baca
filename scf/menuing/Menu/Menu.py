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

    # TODO: rewrite these with any()
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
            result.extend(section.unpacked_menu_entries_optimized)
        return result

    ### PUBLIC METHODS ###

    def change_user_input_to_directive_optimized(self, user_input):
        if self.user_enters_nothing(user_input) and self.default_value:
            return self.conditionally_enclose_in_list(self.default_value)
        elif self.user_enters_argument_range_optimized(user_input):
            return self.handle_argument_range_user_input_optimized(user_input)
        else:
            for number, key, body, return_value, section in self.unpacked_menu_entries:
                body = iotools.strip_diacritics_from_binary_string(body).lower()
                if  (mathtools.is_integer_equivalent_expr(user_input) and int(user_input) == number) or \
                    (user_input == key) or \
                    (3 <= len(user_input) and body.startswith(user_input)):
                    return self.conditionally_enclose_in_list(return_value)

    def conditionally_display_menu(self):
        self.conditionally_clear_terminal()
        self.make_menu_lines()
        self.conditionally_display_lines(self.menu_lines)
        user_response = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        user_input = self.split_multipart_user_response(user_response)
        user_input = iotools.strip_diacritics_from_binary_string(user_input)
        user_input = user_input.lower()
        directive = self.change_user_input_to_directive_optimized(user_input)
        directive = self.strip_default_indicators_from_strings(directive)
        self.session.hide_next_redraw = False
        directive = self.handle_hidden_key(directive)
        return directive

    def conditionally_enclose_in_list(self, expr):
        if self.has_ranged_section:
            return [expr]
        else:
            return expr

    def handle_argument_range_user_input_optimized(self, user_input):
        if not self.has_ranged_section:
            return
        entry_numbers = self.ranged_section.argument_range_string_to_numbers_optimized(user_input)
        if entry_numbers is None:
            return None
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = self.ranged_section.menu_entry_return_values[i]
            result.append(entry)
        return result

    def make_menu_lines(self):
        self.menu_lines = []
        self.menu_lines.extend(self.make_menu_title_lines())
        self.menu_lines.extend(self.make_section_lines())

    def make_menu_title_lines(self):
        menu_lines = []
        if not self._hide_current_run:
            menu_lines.append(iotools.capitalize_string_start(self.session.menu_header))
            menu_lines.append('')
        return menu_lines

    # TODO: rewrite with **kwargs
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
        
    # TODO: globally remove should_clear_terminal (if possible)
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

    # TODO: apply default indicators at display time so this can be completely removed
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

    def user_enters_argument_range_optimized(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and 'default'.startswith(user_input))
