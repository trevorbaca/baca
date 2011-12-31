from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._indent_level = 1
        self.menu_entry_tokens = None
        self.allow_argument_range = False
        self.default_index = None
        self.display_keys = True
        self.number_menu_entries = False
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
    def menu_entry_bodies(self):
        return [self.menu_entry_token_to_key_and_body(x)[1] for x in self.menu_entry_tokens]

    @property
    def menu_entry_keys(self):
        return [self.menu_entry_token_to_key_and_body(x)[0] for x in self.menu_entry_tokens]

    @property
    def menu_entry_return_values(self):
        if self.number_menu_entries:
            return [self.menu_entry_token_to_value(x) for x in self.menu_entry_tokens]

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def allow_argument_range():
        def fget(self):
            return self._allow_argument_range
        def fset(self, allow_argument_range):
            assert isinstance(allow_argument_range, type(True))
            self._allow_argument_range = allow_argument_range
        return property(**locals())

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
    def display_keys():
        def fget(self):
            return self._display_keys
        def fset(self, display_keys):
            assert isinstance(display_keys, type(True))
            self._display_keys = display_keys
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
    def number_menu_entries():
        def fget(self):
            return self._number_menu_entries
        def fset(self, number_menu_entries):
            assert isinstance(number_menu_entries, type(True))
            self._number_menu_entries = number_menu_entries
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

    def is_menu_entry_token(self, expr):
        if isinstance(expr, str):
            return True
        elif isinstance(expr, tuple) and len(expr) == 2:
            return True
        return False
        
    def make_menu_lines(self, all_keys, all_bodies):
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
            if self.number_menu_entries:
                entry_number = entry_index + 1
                menu_line += '{}: '.format(str(entry_number))
            if key and self.display_keys:
                menu_line += '{} ({})'.format(body, key)
            else:
                menu_line += '{}'.format(body)
            menu_lines.append(menu_line)
            all_keys.append(key)
            all_bodies.append(body)
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

    def menu_entry_token_to_value(self, menu_entry_token):
        if isinstance(menu_entry_token, str):
            return menu_entry_token
        elif isinstance(menu_entry_token, tuple):
            return menu_entry_token[1]
        else:
            raise ValueError
