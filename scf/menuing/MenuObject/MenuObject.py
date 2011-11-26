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

    def conditionally_clear_terminal(self):
        if self.session.is_displayable and self.should_clear_terminal:
            self.clear_terminal()

    def confirm(self):
        response = raw_input('Ok? ')
        if not response.lower() == 'y':
            print ''
            return False
        return True

    def edit_client_source(self):
        file_name = self.client[1]
        line_number = self.client[2]
        command = 'vi +%s %s' % (line_number, file_name)
        os.system(command)

    def exec_statement(self):
        statement = raw_input('xcf> ')
        exec('from abjad import *')
        exec('result = %s' % statement)
        print repr(result) + '\n'

    def grep_baca(self):
        response = raw_input('regex> ')
        command = 'grep -Irn "%s" * | grep -v svn' % response
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())

    def handle_hidden_key(self, key):
        if key == 'exec':
            self.exec_statement()
        elif key == 'grep':
            self.grep_baca()
        elif key == 'here':
            self.edit_client_source()
        elif key == 'hidden':
            return self.show_hidden_items()
        elif key == 'q':
            self.session.user_specified_quit = True
        elif key == 'studio':
            raise StudioException
        elif key == 'where':
            self.show_menu_client()
        else:
            return False
        return True

    def is_string(self, expr):
        return isinstance(expr, str)

    def make_tab(self, n):
        return 4 * n * ' '

    def pop_next_user_response_from_user_input(self):
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return ''
        else:
            user_input = self.session.user_input.split('\n')
            user_response = user_input[0]
            user_input = '\n'.join(user_input[1:])
            self.session.user_input = user_input
            return user_response

    def show_menu_client(self):
        print self.make_tab(1),
        print 'file: %s' % self.where[1]
        print self.make_tab(1),
        print 'line: %s' % self.where[2]
        print self.make_tab(1),
        print 'meth: %s()' % self.where[3]
        print ''

    def show_hidden_items(self):
        hidden_items = []
        hidden_items.extend(self.default_hidden_items)
        hidden_items.extend(self.hidden_items)
        for section in getattr(self, 'menu_sections', []):
            hidden_items.extend(section.hidden_items)
        hidden_items.sort()
        menu_lines = []
        for key, value in hidden_items:
            menu_line = self.make_tab(self.indent_level) + ' '
            menu_line += '%s: %s' % (key, value)
            menu_lines.append(menu_line)
        menu_lines.append('')
        if self.session.test is None:
            for menu_line in menu_lines:
                print menu_line
            return True
        elif self.session.test == 'menu_lines':
            return menu_lines
        else:
            raise ValueError
