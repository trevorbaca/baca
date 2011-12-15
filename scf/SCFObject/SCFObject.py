from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from baca.scf.Session import Session
import inspect
import os
import pprint
import re
import readline


class SCFObject(object):
    
    def __init__(self, session=None):
        self.session = session

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def breadcrumbs(self):
        return self.session.breadcrumbs

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
                self._session = Session()
            else:
                assert isinstance(session, type(Session()))
                self._session = session
        return property(**locals())

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    @property
    def transcript(self):
        return self.session.transcript

    @property
    def transcript_signature(self):
        return self.session.transcript_signature

    @property
    def ts(self):
        return self.transcript_signature

    ### PUBLIC METHODS ###

    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    def confirm(self):
        response = self.handle_raw_input('ok?', include_chevron=False)
        if not response.lower() == 'y':
            self.display_cap_lines([''])
            return False
        return True

    def display_cap_lines(self, lines):
        self.display_lines(lines, capitalize_first_character=True)
        
    def display_lines(self, lines, capitalize_first_character=False):
        assert isinstance(lines, list)
        if capitalize_first_character:
            lines = [iotools.capitalize_string_start(line) for line in lines]
        if lines:
            self.session.append_lines_to_transcript(lines)
        if self.session.is_displayable:
            for line in lines:
                print line

    def edit_source_file(self):
        command = 'vi {}'.format(self.source_file_name)
        os.system(command)

    def handle_raw_input(self, prompt, include_chevron=True):
        prompt = iotools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + '> '
        else:
            prompt = prompt + ' '
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        menu_chunk = []
        menu_chunk.append('{}{}'.format(prompt, user_response))
        menu_chunk.append('')
        self.session.append_lines_to_transcript(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, prompt, default=None):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt)
        finally:
            readline.set_startup_hook()

    def integer_range_string_to_numbers(self, integer_range_string, range_start=None, range_stop=None):
        numbers = []
        range_parts = integer_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(range_start, range_stop + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start, stop = int(start), int(stop)
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = int(range_part)
                numbers.append(number)
        return numbers

    def is_boolean(self, expr):
        return isinstance(expr, type(True))

    def is_integer(self, expr):
        return isinstance(expr, int)

    def is_integer_range_string(self, expr):
        pattern = re.compile('^(\d+(-\d+)?)(,\d+(-\d+)?)*$')
        return expr == 'all' or pattern.match(expr) is not None

    def is_markup(self, expr):
        return isinstance(expr, markuptools.Markup)

    def is_named_chromatic_pitch(self, expr):
        return isinstance(expr, pitchtools.NamedChromaticPitch)

    def is_negative_integer(self, expr):
        return self.is_integer(expr) and expr < 0

    def is_nonnegative_integer(self, expr):
        return self.is_integer(expr) and expr <= 0

    def is_nonpositive_integer(self, expr):
        return self.is_integer(expr) and 0 <= expr

    def is_pitch_range_or_none(self, expr):
        return isinstance(expr, (pitchtools.PitchRange, type(None)))

    def is_positive_integer(self, expr):
        return self.is_integer(expr) and 0 < expr

    def is_string(self, expr):
        return isinstance(expr, str)

    def is_string_or_none(self, expr):
        return isinstance(expr, (str, type(None)))

    def make_new_getter(self, where=None):
        import baca
        return baca.scf.menuing.UserInputGetter(where=where, session=self.session)

    def make_new_menu(self, where=None):
        import baca
        menu = baca.scf.menuing.Menu(where=where, session=self.session)
        section = menu.make_new_section()
        return menu, section

    def pt(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    def pop_next_user_response_from_user_input(self):
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return None
        else:
            if '\n' in self.session.user_input:
                user_input = self.session.user_input.split('\n')
                user_response = user_input[0]
                user_input = '\n'.join(user_input[1:])
            else:
                user_input = self.session.user_input.split(' ')
                user_response = user_input[0]
                user_input = ' '.join(user_input[1:])
            user_response = user_response.replace('_', ' ')
            self.session.user_input = user_input
            return user_response

    def print_not_implemented(self):
        lines = []
        lines.append('not yet implemented.')
        lines.append('')
        self.display_cap_lines(lines)
        self.proceed()
        return True, None

    def proceed(self):
        response = self.handle_raw_input('press return to continue.', include_chevron=False)
        self.conditionally_clear_terminal()

    def query(self, prompt):
        response = handle_raw_input(prompt)
        return response.lower().startswith('y')

    def where(self):
        return inspect.stack()[1]
