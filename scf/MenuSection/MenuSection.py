class MenuSection(object):

    def __init__(self, menu_section_title='', lines_to_list=None,
        menu_section_entries=None, sentence_length_items=None, indent_level=1, 
        hide_menu=False, layout='list'):
        self.menu_section_title = menu_section_title
        self.lines_to_list = lines_to_list
        self.menu_section_entries = menu_section_entries
        self.sentence_length_items = sentence_length_items
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
                print self.menu_section_title
                print ''

    def _print_tab(self, n):
        if 0 < n:
            print self._tab(n),

    def _tab(self, n):
        return 4 * n * ' '
    
    ### PUBLIC ATTRIBUTES ###

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
        for line in self.lines_to_list:
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                print line
        if self.lines_to_list:
            if not self.hide_menu:
                print ''
        for key, value in self.menu_section_entries:
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                if self.layout == 'list':
                    print '%s: %s' % (key, value)
                elif self.layout == 'line':
                    print '%s: %s' % (key, value),
            all_keys.append(key)
            all_values.append(value)
        if self.menu_section_entries:
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
