from abjad.tools import iotools
import os
import subprocess


class _MenuObject(object):

    def __init__(self, client=None, menu_header=None, menu_body=None):
        self.client = client
        self.menu_header = menu_header
        self.menu_body = menu_body

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @apply
    def client():
        def fget(self):
            return self._client
        def fset(self, client):
            self._client = client
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

    def grep_baca(self):
        response = raw_input('regex> ')
        command = 'grep -Irn "%s" * | grep -v svn' % response
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())

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

    def tab(self, n):
        return 4 * n * ' '
