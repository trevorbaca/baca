


class MenuSectionSpecifier(object):

    def __init__(self, menu_section_title='', menu_section_entries=None, 
        sentence_length_items=None, indent_level=1):
        self.menu_section_title = menu_section_title
        self.menu_section_entries = menu_section_entries
        self.sentence_length_items = sentence_length_items
        self.indent_level = indent_level

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    def _display_menu_section_title(self):
        if self.menu_section_title:
            self._print_tab(self.indent_level)
            print self.menu_section_title
            print ''

    def _print_tab(self, n):
        if 0 < n:
            print self._tab(n),

    def _tab(self, n):
        return 4 * n * ' '
    
    ### PUBLIC ATTRIBUTES ###

    @apply
    def indent_level():
        def fget(self):
            return self._indent_level
        def fset(self, indent_level):
            assert isinstance(indent_level, int)
            self._indent_level = indent_level
        return property(**locals())

    @apply
    def menu_section_entries():
        def fget(self):
            return self._menu_section_entries
        def fset(self, menu_section_entries):
            if menu_section_entries is None:
                self._menu_section_entries = []
            else:
                self._menu_section_entries = menu_section_entries[:]
        return property(**locals())

    @apply
    def menu_section_title():
        def fget(self):
            return self._menu_section_title
        def fset(self, menu_section_title):
            assert isinstance(menu_section_title, str)
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
        for key, value in self.menu_section_entries:
            self._print_tab(self.indent_level),
            print '%s: %s' % (key, value)
            all_keys.append(key)
            all_values.append(value)
        if self.menu_section_entries:
            print ''
        for key, value in self.sentence_length_items:
            self._print_tab(self.indent_level),
            print '%s: %s' % (key, value)
            all_keys.append(key)
            all_values.append(value)
        if self.sentence_length_items:
            print ''
