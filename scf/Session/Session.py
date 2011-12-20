from baca.scf.Transcript import Transcript


class Session(object):
    
    def __init__(self, user_input=None):
        self._command_history = []
        self._complete_transcript = Transcript()
        self._session_once_had_user_input = False
        self.backtrack_preservation_is_active = False
        self.breadcrumbs = []
        self.current_score_package_short_name = None
        self.display_pitch_ranges_with_numbered_pitches = False
        self.dump_transcript = False
        self.hide_next_redraw = False
        self.initial_user_input = user_input
        self.is_backtracking_locally = False
        self.is_backtracking_to_score = False
        self.is_backtracking_to_studio = False
        self.is_navigating_to_next_score = False
        self.is_navigating_to_prev_score = False
        self.last_command_was_composite = False
        self.scores_to_show = 'active'
        self.transcribe_next_command = True
        self.user_input = user_input
        self.user_specified_quit = False

    ### OVERLOADS ###

    def __bool__(self):
        return True

    def __repr__(self):
        summary = []
        if self.initial_user_input is not None:
            summary.append('initial_user_input={!r}'.format(self.initial_user_input))
        if self.user_input is not None:
            summary.append('user_input={!r}'.format(self.user_input))
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    def __str__(self):
        return '\n'.join(self.formatted_attributes)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def backtrack_preservation_is_active():
        def fget(self):
            return self._backtrack_preservation_is_active
        def fset(self, backtrack_preservation_is_active):
            assert isinstance(backtrack_preservation_is_active, bool)
            self._backtrack_preservation_is_active = backtrack_preservation_is_active
        return property(**locals())

    @property
    def command_history(self):
        return self._command_history

    @property
    def command_history_string(self):
        return ' '.join(self.command_history)

    @property
    def complete_transcript(self):
        return self._complete_transcript

    @apply
    def current_score_package_short_name():
        def fget(self):
            return self._current_score_package_short_name
        def fset(self, current_score_package_short_name):
            assert isinstance(current_score_package_short_name, (str, type(None)))
            self._current_score_package_short_name = current_score_package_short_name
        return property(**locals())

    @apply
    def dump_transcript():
        def fget(self):
            return self._dump_transcript
        def fset(self, dump_transcript):
            assert isinstance(dump_transcript, bool)
            self._dump_transcript = dump_transcript
        return property(**locals())

    @property
    def formatted_attributes(self):
        result = []
        result.append('initial_user_input: {!r}'.format(self.initial_user_input))
        result.append('breadcrumbs: {!r}'.format(self.breadcrumbs))
        result.append('scores_to_show: {!r}'.format(self.scores_to_show))
        result.append('user_input: {!r}'.format(self.user_input))
        return result

    @apply
    def hide_next_redraw():
        def fget(self):
            return self._hide_next_redraw
        def fset(self, hide_next_redraw):
            assert isinstance(hide_next_redraw, bool)
            self._hide_next_redraw = hide_next_redraw
        return property(**locals())

    @apply
    def is_backtracking_locally():
        def fget(self):
            return self._is_backtracking_locally
        def fset(self, is_backtracking_locally):
            assert isinstance(is_backtracking_locally, bool)
            self._is_backtracking_locally = is_backtracking_locally
        return property(**locals())

    @apply
    def is_backtracking_to_score():
        def fget(self):
            return self._is_backtracking_to_score
        def fset(self, is_backtracking_to_score):
            assert isinstance(is_backtracking_to_score, bool)
            self._is_backtracking_to_score = is_backtracking_to_score
        return property(**locals())

    @apply
    def is_backtracking_to_studio():
        def fget(self):
            return self._is_backtracking_to_studio
        def fset(self, is_backtracking_to_studio):
            assert isinstance(is_backtracking_to_studio, bool)
            self._is_backtracking_to_studio = is_backtracking_to_studio
        return property(**locals())

    @property
    def is_complete(self):
        return self.user_specified_quit

    @property
    def is_displayable(self):
        return not self.user_input

    @property
    def is_navigating_to_sibling_score(self):
        if self.is_navigating_to_next_score:
            return True
        if self.is_navigating_to_prev_score:
            return True
        return False

    @property
    def last_semantic_command(self):
        for command in reversed(self.command_history):
            if not command.startswith('.'):
                return command

    @property
    def menu_header(self):
        if self.breadcrumbs:
            return ' - '.join(self.breadcrumbs)
        else:
            return ''

    @property
    def output_directory(self):
        return '/Users/trevorbaca/.scf/output'

    @property
    def session_once_had_user_input(self):
        return self._session_once_had_user_input

    @property
    def transcript(self):
        return self.complete_transcript.short_transcript

    @apply
    def user_input():
        def fget(self):
            return self._user_input
        def fset(self, user_input):
            assert isinstance(user_input, (str, type(None)))
            self._user_input = user_input
            if isinstance(user_input, str):
                self._session_once_had_user_input = True
        return property(**locals())

    @property
    def user_input_is_consumed(self):
        if self.session_once_had_user_input:
            if self.user_input is None:
                return True
        return False

    @apply
    def transcribe_next_command():
        def fget(self):
            return self._transcribe_next_command
        def fset(self, transcribe_next_command):
            assert isinstance(transcribe_next_command, bool)
            self._transcribe_next_command = transcribe_next_command
        return property(**locals())

    @apply
    def user_specified_quit():
        def fget(self):
            return self._user_specified_quit
        def fset(self, user_specified_quit):
            assert isinstance(user_specified_quit, bool)
            self._user_specified_quit = user_specified_quit
        return property(**locals())

    ### PUBLIC METHODS ###

    def backtrack(self):
        if self.is_complete:
            return True
        elif self.is_backtracking_to_studio:
            return True
        elif self.is_backtracking_to_score:
            return True
        elif self.is_backtracking_locally and self.backtrack_preservation_is_active:
            return True
        elif self.is_backtracking_locally and not self.backtrack_preservation_is_active:
            self.is_backtracking_locally = False
            return True
            
    def clean_up(self):
        if self.dump_transcript:
            self.complete_transcript.write_to_disk(self.output_directory)
