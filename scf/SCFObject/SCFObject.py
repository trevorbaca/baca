from abjad.tools import iotools
import inspect
import os
import pprint
import readline


class SCFObject(object):
    
    def __init__(self, session=None):
        self.session = session

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def Menu(self):
        import baca
        return baca.scf.menuing.Menu

    @property
    def MenuSection(self):
        import baca
        return baca.scf.menuing.MenuSection

    @property
    def Session(self):
        import baca
        return baca.scf.Session

    @property
    def UserInputGetter(self):
        import baca
        return baca.scf.menuing.UserInputGetter

    @property
    def class_name(self):
        return type(self).__name__

    @property
    def help_item_width(self):
        return 5

    @property
    def helpers(self):
        from baca.scf import helpers
        return helpers

    @property
    def spaced_class_name(self):
        spaced_class_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(self.class_name)
        spaced_class_name = spaced_class_name.replace('_', ' ')
        return spaced_class_name

    @apply
    def session():
        def fget(self):
            return self._session
        def fset(self, session):
            if session is None:
                self._session = self.Session()
            else:
                assert isinstance(session, type(self.Session()))
                self._session = session
        return property(**locals())

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    ### PUBLIC METHODS ###

    def conditionally_clear_terminal(self):
        if self.session.is_displayable and self.should_clear_terminal:
            iotools.clear_terminal()

    def confirm(self):
        response = self.handle_raw_input('Ok?')
        if not response.lower() == 'y':
            self.display_lines([''])
            return False
        return True

    def display_lines(self, lines):
        assert isinstance(lines, list)
        if lines:
            self.session.transcript.append(lines[:])
        if self.session.is_displayable:
            for line in lines:
                print line

    def edit_source_file(self):
        command = 'vi {}'.format(self.source_file_name)
        os.system(command)

    def handle_raw_input(self, prompt):
        prompt = prompt + '> '
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        menu_chunk = []
        menu_chunk.append('{}{}'.format(prompt, user_response))
        menu_chunk.append('')
        self.session.transcript.append(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, prompt, default=''):
        if default == 'None':
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return handle_raw_input(prompt)
        finally:
            readline.set_startup_hook()

    def make_new_getter(self, where=None):
        return self.UserInputGetter(where=where, session=self.session)

    def make_new_menu(self, where=None):
        return self.Menu(where=where, session=self.session)

    def pmc(self):
        pprint.pprint(self.session.transcript)

    def pop_next_user_response_from_user_input(self):
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return None
        else:
            user_input = self.session.user_input.split('\n')
            user_response = user_input[0]
            user_input = '\n'.join(user_input[1:])
            self.session.user_input = user_input
            return user_response

    def print_not_implemented(self):
        lines = []
        lines.append('Not yet implemented.')
        lines.append('')
        self.display_lines(lines)
        self.proceed()
        return True, None

    def proceed(self):
        response = handle_raw_input('Press return to continue')
        self.conditionally_clear_terminal()

    def query(self, prompt):
        response = handle_raw_input(prompt)
        return response.lower().startswith('y')

    def where(self):
        return inspect.stack()[1]
