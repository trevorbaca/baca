from abjad.tools import iotools
from baca.scf.SCFObject.SCFObject import SCFObject
from baca.scf.exceptions import StudioException
import os
import subprocess


class MenuObject(SCFObject):

    def __init__(self, session=None, where=None):
        SCFObject.__init__(self, session=session)
        self.hidden_items = None
        self.indent_level = 1
        self.prompt_default = None
        self.should_clear_terminal = False
        self.where = where

    ### PUBLIC ATTRIBUTES ###

    @property
    def default_hidden_items(self):
        default_hidden_items = []
        if getattr(self, 'include_back', False):
            default_hidden_items.append(('b', 'back'))
        default_hidden_items.append(('grep', 'grep baca directories'))
        default_hidden_items.append(('here', 'edit client source'))
        default_hidden_items.append(('hidden', 'show hidden items'))
        default_hidden_items.append(('q', 'quit'))
        default_hidden_items.append(('redraw', 'redraw'))
        default_hidden_items.append(('exec', 'exec statement'))
        default_hidden_items.append(('next', 'next score'))
        default_hidden_items.append(('prev', 'prev score'))
        default_hidden_items.append(('score', 'return to score'))
        default_hidden_items.append(('studio', 'return to studio'))
        default_hidden_items.append(('where', 'show menu client'))
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
    def indent_level():
        def fget(self):
            return self._indent_level
        def fset(self, indent_level):
            assert isinstance(indent_level, int)
            self._indent_level = indent_level
        return property(**locals())

    @apply
    def prompt_default():
        def fget(self):
            return self._prompt_default
        def fset(self, prompt_default):
            assert isinstance(prompt_default, (str, type(None)))
            self._prompt_default = prompt_default
        return property(**locals())

    @apply
    def should_clear_terminal():
        def fget(self):
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, type(True))
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    @apply
    def where():
        def fget(self):
            return self._where
        def fset(self, where):
            self._where = where
        return property(**locals())

    ### PUBLIC METHODS ###

    def conditionally_clear_terminal(self):
        if self.should_clear_terminal:
            SCFObject.conditionally_clear_terminal(self)

    def edit_client_source_file(self):
        file_name = self.where[1]
        line_number = self.where[2]
        command = 'vi +{} {}'.format(line_number, file_name)
        os.system(command)

    def exec_statement(self):
        lines = []
        statement = self.handle_raw_input('XCF')
        exec('from abjad import *')
        try:
            exec('result = {}'.format(statement))
            lines.append('{!r}'.format(result))
        except:
            lines.append('expression not executable.')
        lines.append('')
        self.display_cap_lines(lines)
        self.session.hide_next_redraw = True

    def grep_baca(self):
        regex = self.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display_lines(lines)

    def handle_hidden_key(self, key):
        '''Method consumes key (when possible).
        '''
        if key == 'b':
            self.session.is_backtracking_locally = True
        elif key == 'exec':
            self.exec_statement()
        elif key == 'grep':
            self.grep_baca()
        elif key == 'here':
            self.edit_client_source_file()
        elif key == 'hidden':
            self.show_hidden_menu_items()
        elif key == 'next':
            self.session.is_navigating_to_next_score = True
            self.session.is_backtracking_to_studio = True
        elif key == 'prev':
            self.session.is_navigating_to_prev_score = True
            self.session.is_backtracking_to_studio = True
        elif key == 'q':
            self.session.user_specified_quit = True
        elif isinstance(key, str) and 3 <= len(key) and 'score'.startswith(key):
            self.session.is_backtracking_to_score = True
        elif isinstance(key, str) and 3 <= len(key) and 'studio'.startswith(key):
            self.session.is_backtracking_to_studio = True
        elif key == 'where':
            self.show_menu_client()
        else:
            return key

    def make_is_integer_in_closed_range(self, start, stop):
        return lambda expr: self.is_integer(expr) and start <= expr <= stop

    def make_tab(self, n):
        return 4 * n * ' '

    def show_menu_client(self):
        lines = []
        lines.append('{} file: {}'.format(self.make_tab(1), self.where[1]))
        lines.append('{} line: {}'.format(self.make_tab(1), self.where[2]))
        lines.append('{} meth: {}'.format(self.make_tab(1), self.where[3]))
        lines.append('')
        self.display_lines(lines)
        self.session.hide_next_redraw = True

    def show_hidden_menu_items(self):
        hidden_items = []
        hidden_items.extend(self.default_hidden_items)
        hidden_items.extend(self.hidden_items)
        for section in getattr(self, 'sections', []):
            hidden_items.extend(section.hidden_items)
        hidden_items.sort()
        menu_lines = []
        for key, value in hidden_items:
            menu_line = self.make_tab(self.indent_level) + ' '
            #menu_line += '{}: {}'.format(key, value)
            menu_line += '{} ({})'.format(value, key)
            menu_lines.append(menu_line)
        menu_lines.append('')
        self.display_lines(menu_lines)
        self.session.hide_next_redraw = True
