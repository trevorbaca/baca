from baca.scf.SCFObject.SCFObject import SCFObject
from baca.scf.exceptions import StudioException
from abjad.tools import iotools
import os
import subprocess


class MenuObject(SCFObject):

    def __init__(self, hidden_items=None, indent_level=1, session=None, 
        should_clear_terminal=False, where=None):
        SCFObject.__init__(self, session=session)
        self.hidden_items = hidden_items
        self.indent_level = indent_level
        self.should_clear_terminal = should_clear_terminal
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

    def edit_client_source_file(self):
        file_name = self.client[1]
        line_number = self.client[2]
        command = 'vi +{} {}'.format(line_number, file_name)
        os.system(command)

    def exec_statement(self):
        statement = self.handle_raw_input('xcf')
        exec('from abjad import *')
        exec('result = {}'.format(statement))
        line = '{!r}\n'.format(result)
        self.display_lines([line])

    def grep_baca(self):
        regex = self.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display_lines(lines)

    def handle_hidden_key(self, key):
        if key == 'exec':
            self.exec_statement()
        elif key == 'grep':
            self.grep_baca()
        elif key == 'here':
            self.edit_client_source_file()
        elif key == 'hidden':
            self.show_hidden_menu_items()
        elif key == 'q':
            self.session.user_specified_quit = True
        elif key == 'where':
            self.show_menu_client()
        else:
            return False
        return True

    def is_string(self, expr):
        return isinstance(expr, str)

    def make_tab(self, n):
        return 4 * n * ' '

    def show_menu_client(self):
        lines = []
        lines.append('{} file: {}'.format(self.make_tab(1), self.where[1]))
        lines.append('{} line: {}'.format(self.make_tab(1), self.where[2]))
        lines.append('{} meth: {}'.format(self.make_tab(1), self.where[3]))
        lines.append('')
        self.display_lines(lines)

    def show_hidden_menu_items(self):
        hidden_items = []
        hidden_items.extend(self.default_hidden_items)
        hidden_items.extend(self.hidden_items)
        for section in getattr(self, 'menu_sections', []):
            hidden_items.extend(section.hidden_items)
        hidden_items.sort()
        menu_lines = []
        for key, value in hidden_items:
            menu_line = self.make_tab(self.indent_level) + ' '
            menu_line += '{}: {}'.format(key, value)
            menu_lines.append(menu_line)
        menu_lines.append('')
        self.display_lines(menu_lines)
