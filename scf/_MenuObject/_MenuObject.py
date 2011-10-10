from abjad.tools import iotools


class _MenuObject(object):

    def __init__(self, menu_header=None, menu_body=None):
        self.menu_header = menu_header
        self.menu_body = menu_body

    ### PUBLIC ATTRIBUTES ###

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
            return ''

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
