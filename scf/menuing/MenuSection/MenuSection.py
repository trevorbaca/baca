from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self.default_index = None
        self.entries_include_display_string = False # temporary hack
        self.entry_prefix = None
        self.items_to_number = None
        self.keyed_menu_entry_tuples = None
        self.number_menu_entries = False
        self.section_title = None

    ### PUBLIC ATTRIBUTES ###

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

    @apply
    def items_to_number():
        def fget(self):
            return self._items_to_number
        def fset(self, items_to_number):
            if items_to_number is None:
                self._items_to_number = []
            else:
                self._items_to_number = list(items_to_number)
        return property(**locals())

    @apply
    def keyed_menu_entry_tuples():
        def fget(self):
            return self._keyed_menu_entry_tuples
        def fset(self, keyed_menu_entry_tuples):
            if keyed_menu_entry_tuples is None:
                self._keyed_menu_entry_tuples = []
            else:
                self._keyed_menu_entry_tuples = keyed_menu_entry_tuples[:]
        return property(**locals())

    @property
    def menu_values(self):
        if self.number_menu_entries:
            return [x[1] for x in self.keyed_menu_entry_tuples]
        elif self.items_to_number:
            return self.items_to_number[:]

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

    def make_menu_lines(self, all_keys, all_values, all_display_strings):
        '''Display strings will be retired during migration.
        After migration the meaning of keys and values will be as follows.
        KEYS will be those things to be ultimately returned a menu by which
        calling code will be able uniquely to execute a resultant action;
        keys will also be those things optionally shown in parentheses in each entry;
        keys are designed to be textual (as opposed to numeric);
        not every entry need have a key because entries may be numbered instead of keyed;
        note that entries may be both numbered and keyed.
        BODIES will be those things shown in each entry;
        values are mandatory and every entry must be supplied with a value.
        Display strings will be retired.

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
        for i, value in enumerate(self.items_to_number):
            if isinstance(value, tuple):
                assert len(value) == 2
                display_string, return_value = value
            else:
                display_string = return_value = value
            key = str(i + 1)
            menu_line = self.make_tab(self.indent_level) + ' '
            prefix = self.entry_prefix
            if prefix is not None:
                key = prefix + key
            menu_line += '{}: {}'.format(key, display_string)
            menu_lines.append(menu_line)
            all_keys.append(key)
            all_values.append(return_value)
            all_display_strings.append(display_string)
        if self.items_to_number:
            menu_lines.append('')
        assert all([isinstance(x, tuple) for x in self.keyed_menu_entry_tuples])
        for entry_index, keyed_menu_entry_tuple in enumerate(self.keyed_menu_entry_tuples):
            if len(keyed_menu_entry_tuple) == 2:
                key, value = keyed_menu_entry_tuple
                display_key = True
                display_string = None
            elif len(keyed_menu_entry_tuple) == 3:
#                if self.entries_include_display_string:
#                    key, display_string, display_key = keyed_menu_entry_tuple
#                    value = key
#                else:
#                    key, value, display_key = keyed_menu_entry_tuple
#                    display_string = None
                key, value, display_key = keyed_menu_entry_tuple
                display_string = None
                #print key, value, display_key
            else:
                raise ValueError('keyed menu entry tuples must have length 2 or 3.')
            menu_line = self.make_tab(self.indent_level) + ' '
            if self.number_menu_entries:
                entry_number = entry_index + 1
                menu_line += '{}: '.format(str(entry_number))
                all_keys.append(str(entry_number))
                if self.entries_include_display_string:
                    all_values.append(key)
                else:
                    all_values.append(value)
                all_display_strings.append(display_string)
            if key and display_key:
                menu_line += '{} ({})'.format(value, key)
            else:
                menu_line += '{}'.format(value)
            menu_lines.append(menu_line)
            all_keys.append(key)
            all_values.append(value)
            all_display_strings.append(display_string)
        #print all_keys
        #print all_values
        if self.keyed_menu_entry_tuples:
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
