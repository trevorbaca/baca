from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, default_index=None, entry_prefix=None, hidden_items=None, 
        hide_menu=False, indent_level=1, items_to_number=None, 
        lines_to_list=None, section_title=None, named_pairs=None, 
        sentence_length_items=None):
        self.default_index = default_index
        self.entry_prefix = entry_prefix
        self.hidden_items = hidden_items
        self.hide_menu = hide_menu
        self.indent_level = indent_level
        self.items_to_number = items_to_number
        self.lines_to_list = lines_to_list
        self.section_title = section_title
        self.named_pairs = named_pairs
        self.sentence_length_items = sentence_length_items

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
    def has_default(self):
        return self.default_index is not None

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
    def indent_level():
        def fget(self):
            return self._indent_level
        def fset(self, indent_level):
            assert isinstance(indent_level, int)
            self._indent_level = indent_level
        return property(**locals())

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
    def lines_to_list():
        def fget(self):
            return self._lines_to_list
        def fset(self, lines_to_list):
            if lines_to_list is None:
                self._lines_to_list = []
            else:
                self._lines_to_list = lines_to_list[:]
        return property(**locals())

    @apply
    def named_pairs():
        def fget(self):
            return self._named_pairs
        def fset(self, named_pairs):
            if named_pairs is None:
                self._named_pairs = []
            else:
                self._named_pairs = named_pairs[:]
        return property(**locals())

    @apply
    def entry_prefix():
        def fget(self):
            return self._entry_prefix
        def fset(self, entry_prefix):
            assert isinstance(entry_prefix, (str, type(None)))
            self._entry_prefix = entry_prefix
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
    def sentence_length_items():
        def fget(self):
            return self._sentence_length_items
        def fset(self, sentence_length_items):
            if sentence_length_items is None:
                self._sentence_length_items = []
            else:
                self._sentence_length_items = sentence_length_items[:]
        return property(**locals())

    ### PUBLIC METHODS ###

    def get_default_value(self):
        assert self.has_default
        return self.items_to_number[self.default_index]

    def make_menu_lines(self, all_keys, all_values, all_display_strings):
        menu_lines = []
        menu_lines.extend(self.make_section_title_lines())
        for i, value in enumerate(self.items_to_number):
            if isinstance(value, tuple):
                assert len(value) == 2
                display_string, return_value = value
            else:
                display_string = return_value = value
            key = str(i + 1)
            if not self.hide_menu:
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
            if not self.hide_menu:
                menu_lines.append('')
        for line in self.lines_to_list:
            if not self.hide_menu:
                menu_line = self.make_tab(self.indent_level) + ' ' + line
                menu_lines.append(menu_line)
        if self.lines_to_list:
            if not self.hide_menu:
                menu_lines.append('')
        for key, value in self.named_pairs:
            if self.entry_prefix is not None:
                key = self.entry_prefix + key
            if not self.hide_menu:
                menu_line = self.make_tab(self.indent_level) + ' '
                #menu_line += '{}: {}'.format(key, value)
                menu_line += '{}'.format(value)
            all_keys.append(key)
            all_values.append(value)
            all_display_strings.append(None)
        if self.named_pairs:
            if not self.hide_menu:
                menu_lines.append('')
        for key, value in self.sentence_length_items:
            if not self.hide_menu:
                menu_line = self.make_tab(self.indent_level) + ' '
                #menu_line += '{}: {}'.format(key, value)
                menu_line += '{}'.format(value)
                menu_lines.append(menu_line)
            all_keys.append(key)
            all_values.append(value)
            all_display_strings.append(None)
        if self.sentence_length_items:
            if not self.hide_menu:
                menu_lines.append('')
        for key, value in self.hidden_items:
            all_keys.append(key)
            all_values.append(value)
            all_display_strings.append(None)
        return menu_lines

    def make_section_title_lines(self):
        menu_lines = []
        if not self.hide_menu:
            if self.section_title:
                menu_line = '{} {}'.format(
                    self.make_tab(self.indent_level), iotools.capitalize_string_start(self.section_title))
                menu_lines.append(menu_line)
                menu_lines.append('')
        return menu_lines

    def show_hidden_menu_items(self):
        menu_lines = []
        for key, value in self.hidden_items:
            menu_line = self.make_tab(self.indent_level) + ' '
            #menu_line += '{}: {}'.format(key, value)
            menu_line += '{}'.format(value)
            menu_lines.append(menu_line)
        self.display_lines(menu_lines)
