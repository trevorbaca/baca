from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._indent_level = 1
        self.allow_argument_range = False
        self.default_index = None
        self.display_keys = True
        self.entry_prefix = None
        self.menu_entry_tuples = None
        self.number_menu_entries = False
        self.section_title = None

    ### PUBLIC ATTRIBUTES ###

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
            self._default_index = default_index
        return property(**locals())

    @property
    def default_value(self):
        assert self.has_default
        return self.menu_values[self.default_index]

    @apply
    def display_keys():
        def fget(self):
            return self._display_keys
        def fset(self, display_keys):
            assert isinstance(display_keys, type(True))
            self._display_keys = display_keys
        return property(**locals())

    @apply
    def entry_prefix():
        def fget(self):
            return self._entry_prefix
        def fset(self, entry_prefix):
            assert isinstance(entry_prefix, (str, type(None)))
            self._entry_prefix = entry_prefix
        return property(**locals())

    @property
    def has_default(self):
        return self.default_index is not None

    @property
    def indent_level(self):
        return self._indent_level

    @apply
    def menu_entry_tuples():
        def fget(self):
            return self._menu_entry_tuples
        def fset(self, menu_entry_tuples):
            if menu_entry_tuples is None:
                self._menu_entry_tuples = []
            else:
                self._menu_entry_tuples = menu_entry_tuples[:]
        return property(**locals())

    @property
    def menu_values(self):
        if self.number_menu_entries:
            return [x[1] for x in self.menu_entry_tuples]

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

    ### PUBLIC METHODS ###

    def make_menu_lines(self, all_keys, all_bodies):
        '''Terms.

        KEYS. Keys are optionally shown in parentheses in each entry;
        keys are designed to be textual instead of numeric;
        not every entry need have a key because entries may be numbered instead of keyed;
        note that entries may be both numbered and keyed.

        BODIES. Bodies are those things shown in each entry;
        values are mandatory and every entry must be supplied with a value.
        Display strings will be retired.

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
        assert all([isinstance(x, tuple) and len(x) == 2 for x in self.menu_entry_tuples])
        for entry_index, menu_entry_tuple in enumerate(self.menu_entry_tuples):
            key, body = menu_entry_tuple
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
        if self.menu_entry_tuples:
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
