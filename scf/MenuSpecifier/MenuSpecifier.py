from baca.scf.StudioException import StudioException
from baca.scf.MenuObject import MenuObject
from baca.scf.SCFObject import SCFObject
import os


class MenuSpecifier(MenuObject, SCFObject):

    def __init__(self, menu_header=None, menu_body=None, score_title=None, 
        menu_sections=None, items_to_number=None, sentence_length_items=None, 
        named_pairs=None, secondary_named_pairs=None, include_back=True, 
        include_studio=True, indent_level=1, item_width = 11, 
        should_clear_terminal=True, hide_menu=False):
        MenuObject.__init__(self, menu_header=menu_header, menu_body=menu_body)
        self.score_title = score_title
        self.menu_sections = menu_sections
        self.items_to_number = items_to_number
        self.sentence_length_items = sentence_length_items
        self.named_pairs = named_pairs
        self.secondary_named_pairs = secondary_named_pairs
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
        if self.include_studio:
            all_keys.append('S')
            all_values.append('studio')
        all_keys.append('x')
        all_values.append('exec')
        
    def _display_footer_items(self, all_keys, all_values):
        if not self.hide_menu:
            self._print_tab(self.indent_level)
        footer_pairs = self._get_footer_pairs()
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

    def _display_menu(self, score_title=None):
        if self.should_clear_terminal:
            self.clear_terminal()
        all_keys, all_values = [], []
        self._display_menu_title(score_title=score_title)
        self._display_menu_sections(all_keys, all_values)
        self._display_items_to_number(all_keys, all_values)
        self._display_sentence_length_items(all_keys, all_values)
        self._display_named_pairs(self.named_pairs, all_keys, all_values)
        self._display_named_pairs(self.secondary_named_pairs, all_keys, all_values)
        self._display_footer_items(all_keys, all_values)
        self._add_hidden_menu_items(all_keys, all_values)
        if not self.hide_menu:
            print ''
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
        
    def _display_menu_title(self, score_title=None):
        if self.menu_title:
            if not self.hide_menu:
                if score_title is not None:
                    menu_title = '%s - %s' % (score_title, self.menu_title.lower())
                elif getattr(self, 'score_title', None) is not None:
                    menu_titlte = '%s - %s' % (self.score_title, self.menu_title.lower())
                else:
                    menu_title = self.menu_title
                menu_title = menu_title.capitalize()
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
        footer_pairs = [
            ('q', 'quit'),
            ('w', 'redraw'),
            #('x', 'exec'),
            ]
        if self.include_back:
            footer_pairs.append(('b', 'back'))
        footer_pairs.sort()
        return footer_pairs

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
                self._items_to_number = items_to_number
        return property(**locals())

    @apply
    def menu_sections():
        def fget(self):
            return self._menu_sections
        def fset(self, menu_sections):
            if menu_sections is None:
                self._menu_sections = []
            else:
                self._menu_sections = menu_sections
        return property(**locals())

    @apply
    def named_pairs():
        def fget(self):
            return self._named_pairs
        def fset(self, named_pairs):
            if named_pairs is None:
                self._named_pairs = []
            else:
                self._named_pairs = named_pairs
        return property(**locals())

    @apply
    def secondary_named_pairs():
        def fget(self):
            return self._secondary_named_pairs
        def fset(self, secondary_named_pairs):
            if secondary_named_pairs is None:
                self._secondary_named_pairs = []
            else:
                self._secondary_named_pairs = secondary_named_pairs
        return property(**locals())

    @apply
    def sentence_length_items():
        def fget(self):
            return self._sentence_length_items
        def fset(self, sentence_length_items):
            if sentence_length_items is None:
                self._sentence_length_items = []
            else:
                self._sentence_length_items = sentence_length_items
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

    def display_menu(self, score_title=None):
        should_clear_terminal, hide_menu = True, False
        while True:
            self.should_clear_terminal, self.hide_menu = should_clear_terminal, hide_menu
            key, value = self._display_menu(score_title=score_title)
            should_clear_terminal, hide_menu = False, True
            if key == 'b':
                return key, None
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                should_clear_terminal, hide_menu = True, False
            elif key == 'x':
                self.exec_statement()
            elif key == 'S':
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

    def tab(self, n):
        return 4 * n * ' '
