from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from baca.scf.Session import Session
import inspect
import os
import pprint
import readline
import sys


class SCFObject(object):
    
    def __init__(self, session=None):
        self._session = session or Session()

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def assets_directory(self):
        return os.path.join(self.scf_root_directory, 'assets')

    @property
    def breadcrumb(self):
        return 'SCF object'

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
    def materialpackagemakers_directory_name(self):
        return os.path.join(self.scf_root_directory, 'materialpackagemakers')

    @property
    def materialpackagemakers_package_importable_name(self):
        return self.dot_join([self.scf_package_importable_name, 'materialpackagemakers'])

    @property
    def scf_package_importable_name(self):
        return self.dot_join([self.studio_package_importable_name, 'scf'])

    @property
    def scf_root_directory(self):
        return self.package_importable_name_to_directory_name(self.scf_package_importable_name)

    @property
    def score_materials_package_importable_name_body(self):
        return 'mus.materials'

    @property
    def score_specifiers_package_importable_name_body(self):
        return 'mus.specifiers'

    @property
    def session(self):
        return self._session

    @property
    def sketches_package_importable_name(self):
        return self.dot_join([self.studio_package_importable_name, 'sketches'])

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    @property
    def spaced_class_name(self):
        return iotools.uppercamelcase_to_space_delimited_lowercase(self.class_name)

    @property
    def studio_directory_name(self):
        return self.package_importable_name_to_directory_name(self.studio_package_importable_name)

    @property
    def studio_materials_package_importable_name(self):
        return self.dot_join([self.studio_package_importable_name, 'materials'])

    @property
    def studio_specifiers_package_importable_name(self):
        return self.dot_join([self.studio_package_importable_name, 'specifiers'])

    @property
    def studio_package_importable_name(self):
        return 'baca'

    @property
    def stylesheets_directory_name(self):
        return os.path.join(self.scf_root_directory, 'stylesheets')

    @property
    def stylesheets_package_importable_name(self):
        return self.dot_join([self.scf_package_importable_name, 'stylesheets'])

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

    def backtrack(self):
        return self.session.backtrack()

    def cache_breadcrumbs(self, cache=False):
        if cache:
            self.session.breadcrumb_cache_stack.append(self.session.breadcrumb_stack[:])
            self.session._breadcrumb_stack[:] = []

    def conditionally_add_terminal_newlines(self, lines):
        terminated_lines = []
        for line in lines:
            if not line.endswith('\n'):
                line = line + '\n'
            terminated_lines.append(line)
        terminated_lines = type(lines)(terminated_lines)
        return terminated_lines
        
    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    def confirm(self, prompt_string='ok', include_chevron=False):
        getter = self.make_getter(where=self.where())
        getter.append_yes_no_string(prompt_string)
        result = getter.run(include_chevron=include_chevron)
        if self.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def debug(self, value, annotation=None):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)

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

    def dot_join(self, expr):
        return '.'.join(expr)

    def handle_raw_input(self, prompt, include_chevron=True, include_newline=True, prompt_character='>',
        capitalize_prompt=True):
        if capitalize_prompt:
            prompt = iotools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + prompt_character + ' '
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

    def handle_raw_input_with_default(self, prompt, default=None, include_chevron=True, include_newline=True,
        prompt_character='>', capitalize_prompt=True):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt, include_chevron=include_chevron, 
                include_newline=include_newline, prompt_character=prompt_character,
                capitalize_prompt=capitalize_prompt)
        finally:
            readline.set_startup_hook()

    def make_getter(self, where=None):
        import baca
        return baca.scf.menuing.UserInputGetter(where=where, session=self.session)

    def make_menu(self, is_hidden=False, is_internally_keyed=False, is_keyed=True, 
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False, where=None):
        import baca
        menu = baca.scf.menuing.Menu(where=where, session=self.session)
        section = menu.make_section(
            is_hidden=is_hidden, is_internally_keyed=is_internally_keyed, is_keyed=is_keyed, 
            is_numbered=is_numbered, is_parenthetically_numbered=is_parenthetically_numbered, 
            is_ranged=is_ranged)
        return menu, section

    def module_importable_name_to_full_file_name(self, module_importable_name):
        full_file_name = self.package_importable_name_to_directory_name(module_importable_name) + '.py'
        return full_file_name

    def package_exists(self, package_importable_name):
        assert isinstance(package_importable_name, str)
        directory_name = self.package_importable_name_to_directory_name(package_importable_name)
        return os.path.exists(directory_name)

    def package_importable_name_to_directory_name(self, package_importable_name):
        if package_importable_name is None:
            return
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == self.studio_package_importable_name:
            directory_parts = [os.environ.get('BACA')] + package_importable_name_parts[1:]
        else:
            directory_parts = [os.environ.get('SCORES')] + package_importable_name_parts[:]
        directory = os.path.join(*directory_parts)
        return directory

    def pop_backtrack(self):
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
        #user_response = user_response.replace('_', ' ')
        user_response = user_response.replace('~', ' ')
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
        self.handle_raw_input('press return to continue.', include_chevron=False)
        self.conditionally_clear_terminal()

    def pt(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    def ptc(self):
        self.session.complete_transcript.ptc()

    def push_backtrack(self):
        if self.session.backtracking_stack:
            last_number = self.session.backtracking_stack[-1]
            self.session.backtracking_stack.append(last_number + 1)
        else:
            self.session.backtracking_stack.append(0)

    def push_breadcrumb(self, breadcrumb=None):
        if breadcrumb is not None:
            self.breadcrumb_stack.append(breadcrumb)
        else:
            self.breadcrumb_stack.append(self.breadcrumb)

    def remove_package_importable_name_from_sys_modules(self, package_importable_name):
        '''Total hack. But works.'''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_importable_name, package_importable_name)
        exec(command)

    def restore_breadcrumbs(self, cache=False):
        if cache:
            #self.session._breadcrumb_stack[:] = self.session.cached_breadcrumbs[:]
            self.session._breadcrumb_stack[:] = self.session.breadcrumb_cache_stack.pop()

    def where(self):
        return inspect.stack()[1]
