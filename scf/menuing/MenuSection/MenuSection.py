from abjad.tools import iotools
from abjad.tools import mathtools
from baca.scf.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, is_hidden=False, is_keyed=True, is_numbered=False, is_ranged=False,
        session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._indent_level = 1
        self._is_hidden = is_hidden
        self._is_keyed = is_keyed
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self.menu_entry_tokens = None
        self.default_index = None
        self.section_title = None
        self.use_menu_entry_key_as_menu_entry_return_value = True

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def default_value(self):
        assert self.has_default_value
        return self.menu_entry_return_values[self.default_index]

    @property
    def has_default_value(self):
        return self.default_index is not None

    @property
    def indent_level(self):
        return self._indent_level

    @property
    def is_hidden(self):
        return self._is_hidden

    @property
    def is_keyed(self):
        return self._is_keyed

    @property
    def is_numbered(self):
        return self._is_numbered

    @property
    def is_ranged(self):
        return self._is_ranged

    @property
    def menu_entry_bodies(self):
        return [self.menu_entry_token_to_key_and_body(x)[1] for x in self.menu_entry_tokens]

    @property
    def menu_entry_keys(self):
        return [self.menu_entry_token_to_key_and_body(x)[0] for x in self.menu_entry_tokens]

    @property
    def menu_entry_return_values(self):
        return [self.menu_entry_token_to_menu_entry_return_value(x) for x in self.menu_entry_tokens]

    @property
    def unpacked_menu_entries(self):
        result = []
        for menu_entry_token in self.menu_entry_tokens:
            result.append(self.unpack_menu_entry_token(menu_entry_token))
        return result

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def default_index():
        def fget(self):
            return self._default_index
        def fset(self, default_index):
            assert isinstance(default_index, (int, type(None)))
            if isinstance(default_index, int):
                count = len(self.menu_entry_tokens)
                if default_index < 0:
                    raise ValueError('default index must be positive integer.')
                if count <= default_index:
                    raise ValueError('only {} menu entry tokens in section.'.format(count))
            self._default_index = default_index
        return property(**locals())

    @apply
    def menu_entry_tokens():
        def fget(self):
            return self._menu_entry_tokens
        def fset(self, menu_entry_tokens):
            if menu_entry_tokens is None:
                self._menu_entry_tokens = []
            else:
                self._menu_entry_tokens = menu_entry_tokens[:]
        return property(**locals())

    @apply
    def section_title():
        def fget(self):
            return self._section_title
        def fset(self, section_title):
            assert isinstance(section_title, (str, type(None)))
            self._section_title = section_title
        return property(**locals())

    @apply
    def use_menu_entry_key_as_menu_entry_return_value():
        def fget(self):
            return self._use_menu_entry_key_as_menu_entry_return_value
        def fset(self, use_menu_entry_key_as_menu_entry_return_value):
            assert isinstance(use_menu_entry_key_as_menu_entry_return_value, type(True))
            self._use_menu_entry_key_as_menu_entry_return_value = use_menu_entry_key_as_menu_entry_return_value
        return property(**locals())

    ### PUBLIC METHODS ###

    def argument_range_string_to_numbers(self, argument_range_string):
        '''Return list of positive integers on success. Otherwise none.
        '''
        assert self.menu_entry_tokens
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_entry_tokens) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = self.argument_string_to_number(start)
                stop = self.argument_string_to_number(stop)
                if start is None or stop is None:
                    return
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = self.argument_string_to_number(range_part)
                if number is None:
                    return
                numbers.append(number)
        return numbers

    def argument_string_to_number(self, argument_string):
        '''Return number when successful. Otherwise none.
        '''
        if mathtools.is_integer_equivalent_expr(argument_string):
            menu_number = int(argument_string)
            if menu_number <= len(self.menu_entry_tokens):
                return menu_number
        for menu_index, menu_return_value in enumerate(self.menu_entry_return_values):
            if argument_string == menu_return_value:
                return menu_index + 1
            elif 3 <= len(argument_string) and menu_return_value.startswith(argument_string):
                return menu_index + 1
        for menu_index, menu_key in enumerate(self.menu_entry_keys):
            if argument_string == menu_key:
                return menu_index + 1

    def is_menu_entry_token(self, expr):
        if isinstance(expr, str):
            return True
        elif isinstance(expr, tuple) and len(expr) == 2:
            return True
        return False
        
    def make_menu_lines(self):
        '''KEYS. Keys are optionally shown in parentheses in each entry;
        keys are designed to be textual instead of numeric;
        not every entry need have a key because entries may be numbered instead of keyed;
        note that entries may be both numbered and keyed.

        BODIES. Bodies are those things shown in each entry;
        bodies are mandatory and every entry must be supplied with a body.

        RESULT. Result is the thing ultimately returned by Menu.run().

        Match determination:
        1. Numeric user input checked against numbered entries.
        2. If key exists, textual user input checked for exact match against key.
        3. Textual user input checked for 3-char match against body.
        4. Otherwise, no match found.
        
        Return value resolution:
        Keyed entries (numbered or not) supply key as return value.
        Nonkeyed entries (always numbered) supply body as return value.
        '''
        menu_lines = []
        menu_lines.extend(self.make_section_title_lines())
        assert all([self.is_menu_entry_token(x) for x in self.menu_entry_tokens])
        for entry_index, menu_entry_token in enumerate(self.menu_entry_tokens):
            key, body = self.menu_entry_token_to_key_and_body(menu_entry_token)
            menu_line = self.make_tab(self.indent_level) + ' '
            if self.is_numbered:
                entry_number = entry_index + 1
                menu_line += '{}: '.format(str(entry_number))
            if key and self.is_keyed:
                menu_line += '{} ({})'.format(body, key)
            else:
                menu_line += '{}'.format(body)
            menu_lines.append(menu_line)
        if self.menu_entry_tokens:
            menu_lines.append('')
        return menu_lines

    def make_section_title_lines(self):
        menu_lines = []
        if self.section_title:
            menu_line = '{} {}'.format(
                self.make_tab(self.indent_level), iotools.capitalize_string_start(self.section_title))
            menu_lines.append(menu_line)
            menu_lines.append('')
        return menu_lines

    def menu_entry_token_to_key_and_body(self, menu_entry_token):
        if isinstance(menu_entry_token, str):
            key, body = None, menu_entry_token
        elif isinstance(menu_entry_token, tuple):
            key, body = menu_entry_token
        else:
            raise ValueError
        return key, body

    def menu_entry_token_to_menu_entry_return_value(self, menu_entry_token):
        if isinstance(menu_entry_token, str):
            return menu_entry_token
        elif isinstance(menu_entry_token, tuple):
            if self.use_menu_entry_key_as_menu_entry_return_value:
                return menu_entry_token[0]
            else:
                return menu_entry_token[1]
        else:
            raise ValueError

    def menu_entry_token_to_menu_entry_number(self, menu_entry_token):
        if self.is_numbered:
            for i, token in enumerate(self.menu_entry_tokens):
                if token == menu_entry_token:
                    return i + 1

    # TODO: replace self.menu_entry_token_to_key_and_body() and also
    #       replace self.menu_entry_token_to_menu_entry_return_value().
    # TODO: unpack all menu entry tokens only once at menu runtime.
    def unpack_menu_entry_token(self, menu_entry_token):
        number = self.menu_entry_token_to_menu_entry_number(menu_entry_token)
        key, body = self.menu_entry_token_to_key_and_body(menu_entry_token)
        return_value = self.menu_entry_token_to_menu_entry_return_value(menu_entry_token)
        return number, key, body, return_value
