class MenuSection(object):

    def __init__(self, menu_section_title=None, lines_to_list=None,
        named_pairs=None, entry_prefix=None,
        sentence_length_items=None, items_to_number=None, 
        hidden_items=None, indent_level=1, 
        hide_menu=False, layout='list'):
        self.menu_section_title = menu_section_title
        self.lines_to_list = lines_to_list
        self.named_pairs = named_pairs
        self.entry_prefix = entry_prefix
        self.sentence_length_items = sentence_length_items
        self.items_to_number = items_to_number
        self.hidden_items = hidden_items
        self.indent_level = indent_level
        self.hide_menu = hide_menu
        self.layout = layout

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    def _display_menu_section_title(self):
        if not self.hide_menu:
            if self.menu_section_title:
                self._print_tab(self.indent_level)
                print self.menu_section_title.capitalize()
                print ''

    def _print_tab(self, n):
        if 0 < n:
            print self._tab(n),

    def _tab(self, n):
        return 4 * n * ' '
    
    ### PUBLIC ATTRIBUTES ###

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
    def layout():
        def fget(self):
            return self._layout
        def fset(self, layout):
            assert layout in ('list', 'line')
            self._layout = layout
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
    def menu_section_title():
        def fget(self):
            return self._menu_section_title
        def fset(self, menu_section_title):
            assert isinstance(menu_section_title, (str, type(None)))
            self._menu_section_title = menu_section_title
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

    def display(self, all_keys, all_values):
        self._display_menu_section_title()
        for i, value in enumerate(self.items_to_number):
            if isinstance(value, tuple):
                assert len(value) == 2
                display_string, return_value = value
            else:
                display_string = return_value = value
            key = str(i + 1)
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                prefix = self.entry_prefix
                if prefix is not None:
                    key = prefix + key
                print '%s: %s' % (key, display_string)
            all_keys.append(key)
            all_values.append(return_value)
        if self.items_to_number:
            if not self.hide_menu:
                print ''
        for line in self.lines_to_list:
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                print line
        if self.lines_to_list:
            if not self.hide_menu:
                print ''
        for key, value in self.named_pairs:
            if self.entry_prefix is not None:
                key = self.entry_prefix + key
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                if self.layout == 'list':
                    print '%s: %s' % (key, value)
                elif self.layout == 'line':
                    print '%s: %s' % (key, value),
            all_keys.append(key)
            all_values.append(value)
        if self.named_pairs:
            if not self.hide_menu:
                if self.layout == 'list':
                    print ''
                elif self.layout == 'line':
                    print '\n'
        for key, value in self.sentence_length_items:
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                print '%s: %s' % (key, value)
            all_keys.append(key)
            all_values.append(value)
        if self.sentence_length_items:
            if not self.hide_menu:
                print ''
        for key, value in self.hidden_items:
            all_keys.append(key)
            all_values.append(value)

    def show_hidden_items(self):
        for key, value in self.hidden_items:
            self._print_tab(self.indent_level),
            print '%s: %s' % (key, value)
