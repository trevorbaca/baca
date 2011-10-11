from baca.scf.menuing._MenuObject import _MenuObject
from baca.scf._SCFObject import _SCFObject
from baca.scf.exceptions import StudioException
import os


class Menu(_MenuObject, _SCFObject):

    def __init__(self, client=None, menu_header=None, menu_body=None, 
        menu_sections=None, items_to_number=None, sentence_length_items=None, 
        named_pairs=None, secondary_named_pairs=None, hidden_items=None,
        include_back=True, include_studio=True, indent_level=1, item_width = 11, 
        should_clear_terminal=True, hide_menu=False):
        _MenuObject.__init__(self, menu_header=menu_header, menu_body=menu_body)
        self.client = client
        self.menu_sections = menu_sections
        self.items_to_number = items_to_number
        self.sentence_length_items = sentence_length_items
        self.named_pairs = named_pairs
        self.secondary_named_pairs = secondary_named_pairs
        self.hidden_items = hidden_items
        self.include_back = include_back
        self.include_studio = include_studio
        self.indent_level = indent_level
        self.item_width = item_width
        self.should_clear_terminal = should_clear_terminal
        self.hide_menu = hide_menu

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    def _add_hidden_menu_items(self, all_keys, all_values):
        for key, value in self.default_hidden_items:
            all_keys.append(key)
            all_values.append(value)
        for key, value in self.hidden_items:
            all_keys.append(key)
            all_values.append(value)
        
    def _display_footer_items(self, all_keys, all_values):
        footer_pairs = self._get_footer_pairs()
        if footer_pairs:
            if not self.hide_menu:
                self._print_tab(self.indent_level)
        for key, value in footer_pairs:
            if not self.hide_menu:
                print '%s: %s ' % (key, value.ljust(self.item_width)),
            all_keys.append(key)
            all_values.append(value)
        if footer_pairs:
            if not self.hide_menu:
                print ''

    def _display_items_to_number(self, all_keys, all_values):
        keys = range(1, len(self.items_to_number) + 1)
        keys = [str(x) for x in keys]
        pairs = zip(keys, self.items_to_number)
        for key, value in pairs:
            if not self.hide_menu:
                self._print_tab(self.indent_level),
                print '%s: %s' % (key, value)
            all_keys.append(key)
            all_values.append(value)
        if pairs:
            if not self.hide_menu:
                print ''

    def _display_menu(self):
        if self.should_clear_terminal:
            self.clear_terminal()
        all_keys, all_values = [], []
        self._display_menu_title()
        self._display_menu_sections(all_keys, all_values)
        self._display_items_to_number(all_keys, all_values)
        self._display_sentence_length_items(all_keys, all_values)
        self._display_named_pairs(self.named_pairs, all_keys, all_values)
        self._display_named_pairs(self.secondary_named_pairs, all_keys, all_values)
        self._display_footer_items(all_keys, all_values)
        self._add_hidden_menu_items(all_keys, all_values)
        while True:
            response = raw_input('scf> ')
            print ''
            if response in all_keys:
                break
        pair_dictionary = dict(zip(all_keys, all_values))
        value = pair_dictionary[response]
        return response, value

    def _display_menu_sections(self, all_keys, all_values):
        for menu_section in self.menu_sections:
            menu_section.hide_menu = self.hide_menu
            menu_section.display(all_keys, all_values)
        
    def _display_menu_title(self):
        if self.menu_title:
            if not self.hide_menu:
                menu_title = self.menu_title.capitalize()
                print menu_title
                print ''

    def _display_named_pairs(self, named_pairs, all_keys, all_values):
        if named_pairs:
            if not self.hide_menu:
                self._print_tab(self.indent_level)
            for key, value in named_pairs:
                if not self.hide_menu:
                    print '%s: %s ' % (key, value.ljust(self.item_width)),
                all_keys.append(key)
                all_values.append(value)
            if not self.hide_menu:
                print ''

    def _display_sentence_length_items(self, all_keys, all_values):
        for key, value in self.sentence_length_items:
            if not self.hide_menu:
                self._print_tab(self.indent_level)
                print '%s: %s ' % (key, value)
            all_keys.append(key)
            all_values.append(value)
        if self.sentence_length_items:
            if not self.hide_menu:
                print ''

    def _get_footer_pairs(self):
#        footer_pairs = [
#            ('q', 'quit'),
#            ('w', 'redraw'),
#            ]
#        if self.include_back:
#            footer_pairs.append(('b', 'back'))
        footer_pairs = []
        footer_pairs.sort()
        return footer_pairs

    def _print_tab(self, n):
        if 0 < n:
            print self._tab(n),

    def _tab(self, n):
        return 4 * n * ' '

    ### PUBLIC ATTRIBUTES ###
    
    @apply
    def client():
        def fget(self):
            return self._client
        def fset(self, client):
            from baca.scf._SCFObject import _SCFObject
            assert isinstance(client, (_SCFObject, type(None)))
            self._client = client
        return property(**locals())

    @property
    def default_hidden_items(self):
        default_hidden_items = []
        if self.include_back:
            default_hidden_items.append(('b', 'back'))
        default_hidden_items.append(('client', 'show menu client'))
        default_hidden_items.append(('hidden', 'show hidden items'))
        default_hidden_items.append(('q', 'quit'))
        default_hidden_items.append(('redraw', 'redraw'))
        default_hidden_items.append(('exec', 'exec statement'))
        default_hidden_items.append(('studio', 'return to studio'))
        return default_hidden_items

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
    def include_back():
        def fget(self):
            return self._include_back
        def fset(self, include_back):
            assert isinstance(include_back, type(True))
            self._include_back = include_back
        return property(**locals())

    @apply
    def include_studio():
        def fget(self):
            return self._include_studio
        def fset(self, include_studio):
            assert isinstance(include_studio, type(True))
            self._include_studio = include_studio
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
    def item_width():
        def fget(self):
            return self._item_width
        def fset(self, item_width):
            assert isinstance(item_width, int)
            self._item_width = item_width
        return property(**locals())

    @apply
    def items_to_number():
        def fget(self):
            return self._items_to_number
        def fset(self, items_to_number):
            if items_to_number is None:
                self._items_to_number = []
            else:
                self._items_to_number = items_to_number[:]
        return property(**locals())

    @apply
    def menu_sections():
        def fget(self):
            return self._menu_sections
        def fset(self, menu_sections):
            if menu_sections is None:
                self._menu_sections = []
            else:
                self._menu_sections = menu_sections[:]
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
    def secondary_named_pairs():
        def fget(self):
            return self._secondary_named_pairs
        def fset(self, secondary_named_pairs):
            if secondary_named_pairs is None:
                self._secondary_named_pairs = []
            else:
                self._secondary_named_pairs = secondary_named_pairs[:]
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

    @apply
    def should_clear_terminal():
        def fget(self):
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, type(True))
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    ### PUBLIC METHODS ###

    def display_menu(self):
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            key, value = self._display_menu()
            should_clear_terminal, hide_menu = False, True
            if key == 'b':
                return key, None
            elif key == 'client':
                self.show_menu_client()
            elif key == 'exec':
                self.exec_statement()
            elif key == 'hidden':
                self.show_hidden_items()
            elif key == 'q':
                raise SystemExit
            elif key == 'redraw':
                should_clear_terminal, hide_menu = True, False
            elif key == 'studio':
                raise StudioException
            else:
                return key, value

    def exec_statement(self):
        statement = raw_input('xcf> ')
        exec('from abjad import *')
        exec('result = %s' % statement)
        print repr(result) + '\n'

    def print_tab(self, n):
        if 0 < n:
            print self.tab(n),

    def show_hidden_items(self):
        hidden_items = []
        hidden_items.extend(self.default_hidden_items)
        hidden_items.extend(self.hidden_items)
        for section in self.menu_sections:
            hidden_items.extend(section.hidden_items)
        hidden_items.sort()
        for key, value in hidden_items:
            self._print_tab(self.indent_level),
            print '%s: %s' % (key, value)
        print ''

    def show_menu_client(self):
        print self._tab(1),
        print 'client: %s' % self.client
        print ''

    def tab(self, n):
        return 4 * n * ' '
