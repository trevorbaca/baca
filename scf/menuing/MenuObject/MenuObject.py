from baca.scf._SCFObject._SCFObject import _SCFObject
from baca.scf.exceptions import StudioException
from abjad.tools import iotools
import os
import subprocess


class MenuObject(_SCFObject):

    def __init__(self, client=None, menu_header=None, menu_body=None, hidden_items=None,
        indent_level=1):
        self.client = client
        self.menu_header = menu_header
        self.menu_body = menu_body
        self.hidden_items = hidden_items
        self.indent_level = indent_level

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)
    
    ### PRIVATE METHODS ###

    def _print_tab(self, n):
        if 0 < n:
            print self._tab(n),

    def _tab(self, n):
        return 4 * n * ' '

    ### PUBLIC ATTRIBUTES ###

    @property
    def class_name(self):
        return type(self).__name__

    @apply
    def client():
        def fget(self):
            return self._client
        def fset(self, client):
            self._client = client
        return property(**locals())

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
    def menu_body():
        def fget(self):
            return self._menu_body
        def fset(self, menu_body):
            assert isinstance(menu_body, (str, type(None)))
            self._menu_body = menu_body
        return property(**locals())

    @apply
    def menu_header():
        def fget(self):
            return self._menu_header
        def fset(self, menu_header):
            assert isinstance(menu_header, (str, type(None)))
            self._menu_header = menu_header
        return property(**locals())


    @property
    def menu_title(self):
        if self.menu_header:
            if self.menu_body:
                return '%s - %s' % (self.menu_header, self.menu_body)
            else:
                return self.menu_header
        elif self.menu_body:
            return self.menu_body
        else:
            return None

    @property
    def menu_title_parts(self):
        if self.menu_title:
            return self.menu_title.split(' - ')
        else:
            return

    ### PUBLIC METHODS ###

    def clear_terminal(self):
        iotools.clear_terminal()

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
            self.show_hidden_items()
        elif key == 'q':
            raise SystemExit
        elif key == 'studio':
            raise StudioException
        elif key == 'where':
            self.show_menu_client()
        else:
            return False
        return True

    def print_tab(self, n):
        if 0 < n:
            print self.tab(n),

    def show_menu_client(self):
        print self._tab(1),
        print 'file: %s' % self.client[1]
        print self._tab(1),
        print 'line: %s' % self.client[2]
        print self._tab(1),
        print 'meth: %s()' % self.client[3]
        print ''

    def show_hidden_items(self):
        hidden_items = []
        hidden_items.extend(self.default_hidden_items)
        hidden_items.extend(self.hidden_items)
        for section in getattr(self, 'menu_sections', []):
            hidden_items.extend(section.hidden_items)
        hidden_items.sort()
        for key, value in hidden_items:
            self._print_tab(self.indent_level),
            print '%s: %s' % (key, value)
        print ''

    def tab(self, n):
        return 4 * n * ' '
