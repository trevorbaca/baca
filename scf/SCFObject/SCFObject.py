from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
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
        return self.session.complete_transcript.signature

    @property
    def ts(self):
        return self.transcript_signature

    ### PUBLIC METHODS ###

    def assign_user_input(self, user_input=None):
        if user_input is not None:
            self.session.user_input = user_input

    def append_breadcrumb(self, breadcrumb=None):
        if breadcrumb is not None:
            self.breadcrumbs.append(breadcrumb)
        else:
            self.breadcrumbs.append(self.breadcrumb)

    # TODO: rename 'opt' as 'menu_keys'
    def argument_range_string_to_numbers(self, argument_range_string, menu_items, opt=None):
        '''Return list of positive integers on success. Otherwise none.
        '''
        assert len(menu_items)
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(menu_items) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = self.argument_string_to_number(start, menu_items, opt=opt)
                stop = self.argument_string_to_number(stop, menu_items, opt=opt)
                if start is None or stop is None:
                    return
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = self.argument_string_to_number(range_part, menu_items, opt=opt)
                if number is None:
                    return
                numbers.append(number)
        return numbers

    # TODO: rename 'opt' as 'menu_keys'
    def argument_string_to_number(self, argument_string, menu_items, opt=None):
        '''Return number when successful. Otherwise none.
        '''
        if mathtools.is_integer_equivalent_expr(argument_string):
            menu_number = int(argument_string)
            if menu_number <= len(menu_items):
                return menu_number
        for menu_index, menu_item in enumerate(menu_items):
            if argument_string == menu_item:
                return menu_index + 1
            elif 3 <= len(argument_string) and menu_item.startswith(argument_string):
                return menu_index + 1
        if opt is None:
            return
        for menu_index, menu_key in enumerate(opt):
            if argument_string == menu_key:
                return menu_index + 1

    def backtrack(self):
        return self.session.backtrack()

    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    def conditionally_display_cap_lines(self, lines):
        self.conditionally_display_lines(lines, capitalize_first_character=True)
        
    def conditionally_display_lines(self, lines, capitalize_first_character=False):
        assert isinstance(lines, list)
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [iotools.capitalize_string_start(line) for line in lines]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.complete_transcript.append_lines(lines)
            if self.session.is_displayable:
                for line in lines:
                    print line

    def confirm(self):
        response = self.handle_raw_input('ok?', include_chevron=False)
        if not response.lower() == 'y':
            self.conditionally_display_cap_lines([''])
            return False
        return True

    def edit_source_file(self):
        command = 'vi {}'.format(self.source_file_name)
        os.system(command)

    def handle_raw_input(self, prompt, include_chevron=True):
        prompt = iotools.capitalize_string_start(prompt)
        #print 'rrr!!!'
        if include_chevron:
            prompt = prompt + '> '
        else:
            prompt = prompt + ' '
        #print 'FOO', self.session.is_displayable
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        if self.session.transcribe_next_command:
            self.session.command_history.append(user_response)
        if user_response == '.':
            last_semantic_command = self.session.last_semantic_command
            user_response = last_semantic_command
        if self.session.transcribe_next_command:
            menu_chunk = []
            menu_chunk.append('{}{}'.format(prompt, user_response))
            menu_chunk.append('')
            self.session.complete_transcript.append_lines(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, prompt, default=None):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt)
        finally:
            readline.set_startup_hook()

    def is_valid_argument_range_string_for_argument_list(self, argument_range_string, argument_list):
        if isinstance(argument_range_string, str):
            if self.argument_range_string_to_numbers(argument_range_string, argument_list) is not None:
                return True
        return False

    def is_argument_range_string(self, expr):
        pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
        return pattern.match(expr) is not None

    def is_boolean(self, expr):
        return isinstance(expr, type(True))

    def is_integer(self, expr):
        return isinstance(expr, int)

    def is_integer_or_none(self, expr):
        return expr is None or self.is_integer(expr)

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

    def make_new_menu(self, is_hidden=False, is_keyed=True, is_numbered=False, where=None):
        import baca
        menu = baca.scf.menuing.Menu(where=where, session=self.session)
        section = menu.make_new_section(is_hidden=is_hidden, is_keyed=is_keyed, is_numbered=is_numbered)
        return menu, section

    def pt(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    def ptc(self):
        self.session.complete_transcript.ptc()

    def pop_breadcrumb(self):
        return self.breadcrumbs.pop()

    def pop_next_user_response_from_user_input(self):
        self.session.last_command_was_composite = False
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return None
        elif '\n' in self.session.user_input:
            raise ValueError('no longer implemented.')
        elif self.session.user_input.startswith('{{'):
            index = self.session.user_input.find('}}')
            user_response = self.session.user_input[2:index]
            user_input = self.session.user_input[index+2:].strip()
            self.session.last_command_was_composite = True
        else:
            user_input = self.session.user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input[:i+1]
            rest_parts = user_input[i+1:]
            user_response = ' '.join(first_parts)
            user_input = ' '.join(rest_parts)
        user_response = user_response.replace('_', ' ')
        self.session.user_input = user_input
        return user_response

    def print_not_implemented(self):
        lines = []
        lines.append('not yet implemented.')
        lines.append('')
        self.conditionally_display_cap_lines(lines)
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
