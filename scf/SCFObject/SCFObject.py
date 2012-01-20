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


# TODO: move all self.is_ predicates to MenuObject
class SCFObject(object):
    
    def __init__(self, session=None):
        self._session = session or Session()

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    # TODO: write test
    @property
    def assets_directory(self):
        return os.path.join(self.scf_root_directory, 'assets')

    @property
    def breadcrumb_stack(self):
        return self.session.breadcrumb_stack

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

    # TODO: write test
    @property
    def materialproxies_directory_name(self):
        return os.path.join(self.scf_root_directory, 'materialproxies')

    # TODO: write test
    @property
    def materialproxies_package_importable_name(self):
        return '.'.join([self.scf_package_importable_name, 'materialproxies'])

    # TODO: write test
    @property
    def scf_package_importable_name(self):
        return '.'.join([self.studio_package_importable_name, 'scf'])

    # TODO: write test
    @property
    def scf_root_directory(self):
        return self.package_importable_name_to_directory_name(self.scf_package_importable_name)

    @property
    def score_package_short_names(self):
        result = []
        scores_directory = os.environ.get('SCORES')
        for x in os.listdir(scores_directory):
            if x[0].isalpha():
                result.append(x)
        return result

    @property
    def session(self):
        return self._session

    # TODO: write test
    @property
    def sketches_package_importable_name(self):
        return '.'.join([self.studio_package_importable_name, 'sketches'])

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    @property
    def spaced_class_name(self):
        return iotools.uppercamelcase_to_space_delimited_lowercase(self.class_name)

    # TODO: write test
    @property
    def studio_directory_name(self):
        return self.package_importable_name_to_directory_name(self.studio_package_importable_name)

    # TODO: write test
    @property
    def studio_materials_package_importable_name(self):
        return '.'.join([self.studio_package_importable_name, 'materials'])

    @property
    def studio_package_importable_name(self):
        return 'baca'

    # TODO: write test; change to stylesheets_directory_name
    @property
    def stylesheets_directory(self):
        return os.path.join(self.scf_root_directory, 'stylesheets')

    # TODO: write test
    @property
    def stylesheets_package_importable_name(self):
        '.'.join([self.scf_package_importable_name, 'stylesheets'])

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

    def push_breadcrumb(self, breadcrumb=None):
        if breadcrumb is not None:
            self.breadcrumb_stack.append(breadcrumb)
        else:
            self.breadcrumb_stack.append(self.breadcrumb)

    def backtrack(self):
        return self.session.backtrack()

    def cache_breadcrumbs(self, cache=False):
        self.session.cached_breadcrumbs = []
        if cache:
            self.session.cached_breadcrumbs = self.session.breadcrumb_stack[:]
            self.session._breadcrumb_stack[:] = []

    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    def display(self, lines, capitalize_first_character=True):
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [iotools.capitalize_string_start(line) for line in lines]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.complete_transcript.append_lines(lines)
            if self.session.is_displayable:
                for line in lines:
                    print line

    def confirm(self, prompt_string='ok'):
        getter = self.make_new_getter(where=self.where())
        getter.append_yes_no_string(prompt_string)
        result = getter.run()
        if self.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def debug(self, value, annotation=None):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)

    def edit_source_file(self):
        command = 'vi {}'.format(self.source_file_name)
        os.system(command)

    def handle_raw_input(self, prompt, include_chevron=True, include_newline=True):
        prompt = iotools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + '> '
        else:
            prompt = prompt + ' '
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            if include_newline:
                if not user_response == 'help':
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
            if include_newline:
                if not user_response == 'help':
                    menu_chunk.append('')
            self.session.complete_transcript.append_lines(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, prompt, default=None, include_chevron=True, include_newline=True):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt, include_chevron=include_chevron, include_newline=include_newline)
        finally:
            readline.set_startup_hook()

    def is_valid_argument_range_string_for_argument_list(self, argument_range_string, argument_list):
        from baca.scf.menuing.MenuSection import MenuSection
        if isinstance(argument_range_string, str):
            dummy_section = MenuSection()
            dummy_section.tokens = argument_list[:]
            if dummy_section.argument_range_string_to_numbers(argument_range_string) is not None:
                return True
        return False

    def is_argument_range_string(self, expr):
        pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
        return pattern.match(expr) is not None

    def is_boolean(self, expr):
        return isinstance(expr, bool)

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

    def is_yes_no_string(self, expr):
        return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())

    def make_new_getter(self, where=None):
        import baca
        return baca.scf.menuing.UserInputGetter(where=where, session=self.session)

    def make_new_menu(self, is_hidden=False, is_keyed=True, is_numbered=False, is_ranged=False, where=None):
        import baca
        menu = baca.scf.menuing.Menu(where=where, session=self.session)
        section = menu.make_new_section(
            is_hidden=is_hidden, is_keyed=is_keyed, is_numbered=is_numbered, is_ranged=is_ranged)
        return menu, section

    # TODO: write test
    def package_exists(self, package_importable_name):
        assert isinstance(package_importable_name, str)
        directory_name = self.package_importable_name_to_directory_name(package_importable_name)
        return os.path.exists(directory_name)

    # TODO: write tests
    def package_importable_name_to_directory_name(self, package_importable_name):
        if package_importable_name is None:
            return
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == self.studio_package_importable_name:
            directory_parts = [os.environ.get('BACA')] + package_importable_name_parts[1:]
        elif package_importable_name_parts[0] in os.listdir(os.environ.get('SCORES')):
            directory_parts = [os.environ.get('SCORES')] + package_importable_name_parts[:]
        else:
            raise ValueError('Unknown package importable name {!r}.'.format(package_importable_name))
        directory = os.path.join(*directory_parts)
        return directory

    def pt(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    def ptc(self):
        self.session.complete_transcript.ptc()

    def pop_backtracking(self):
        return self.session.backtracking_stack.pop()

    def pop_breadcrumb(self):
        return self.breadcrumb_stack.pop()

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
        self.display(lines)
        self.proceed()

    def proceed(self, lines=None, prompt=True):
        assert isinstance(lines, (tuple, list, str, type(None)))
        if not prompt:
            return
        if isinstance(lines, str):
            lines = [lines]
        elif lines is None:
            lines = []
        if lines:
            lines.append('')
            self.display(lines)
        response = self.handle_raw_input('press return to continue.', include_chevron=False)
        self.conditionally_clear_terminal()

    # TODO: write tests
    def purview_name_to_directory_name(self, purview_name):
        if purview_name == self.studio_package_importable_name:
            directory_name = self.studio_directory_name
        else:
            directory_name = os.path.join(['Users', 'trevorbaca', 'Documents', 'scores', purview_name])
        if not os.path.exists(directory_name):
            raise ValueError
        return directory_name

    def push_backtracking(self):
        if self.session.backtracking_stack:
            last_number = self.session.backtracking_stack[-1]
            self.session.backtracking_stack.append(last_number + 1)
        else:
            self.session.backtracking_stack.append(0)

    def query(self, prompt):
        response = handle_raw_input(prompt)
        return response.lower().startswith('y')

    def reveal_modules(self):
        command = 'module_names = sys.modules.keys()'
        exec(command)
        module_names = [x for x in module_names if x.startswith(self.score_package_short_name)]
        module_names.sort()
        return module_names

    def restore_breadcrumbs(self, cache=False):
        if cache:
            self.session._breadcrumb_stack[:] = self.session.cached_breadcrumbs[:]

    def where(self):
        return inspect.stack()[1]
