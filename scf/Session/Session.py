import datetime
import os
import time


class Session(object):
    
    def __init__(self, user_input=None):
        self._complete_transcript = []
        self._session_once_had_user_input = False
        self._start_time = self.cur_time
        self.backtrack_preservation_is_active = False
        self.dump_transcript = False
        self.hide_next_redraw = False
        self.initial_user_input = user_input
        self.is_backtracking_locally = False
        self.is_backtracking_to_score = False
        self.is_backtracking_to_studio = False
        self.breadcrumbs = []
        self.scores_to_show = 'active'
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
    def complete_transcript(self):
        return self._complete_transcript

    @property
    def cur_time(self):
        return datetime.datetime.fromtimestamp(time.time())

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
    def start_time(self):
        return self._start_time

    @property
    def transcript(self):
        return [entry[1] for entry in self.complete_transcript]

    @property
    def transcript_signature(self):
        result = []
        result.append(len(self.transcript))
        indices_already_encountered = set([])
        for i in range(len(self.transcript)):
            if i not in indices_already_encountered:
                shared_indices = [i]
                reference_element = self.transcript[i]
                for j, current_element in enumerate(self.transcript):
                    if current_element == reference_element:
                        if i != j:
                            shared_indices.append(j)
                if 1 < len(shared_indices):
                    result.append(tuple(shared_indices))
                indices_already_encountered.update(shared_indices)
        return tuple(result)

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
    def user_specified_quit():
        def fget(self):
            return self._user_specified_quit
        def fset(self, user_specified_quit):
            assert isinstance(user_specified_quit, bool)
            self._user_specified_quit = user_specified_quit
        return property(**locals())

    ### PUBLIC METHODS ###

    def append_lines_to_transcript(self, lines, clear_terminal=None):
        assert isinstance(lines, list)
        assert isinstance(clear_terminal, (type(True), type(None)))
        entry = []
        entry.append(self.cur_time)
        entry.append(lines[:])
        entry.append(clear_terminal)
        self.complete_transcript.append(entry)

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
            self.write_complete_transcript_to_disk()

    def format_transcript_entry(self, entry):
        assert len(entry) == 3
        result = []
        result.append(str(entry[0]))
        if entry[2]:
            result.append('clear_terminal=True')
        for line in entry[1]:
            result.append(line)
        return '\n'.join(result)

    def write_complete_transcript_to_disk(self):
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = os.path.join(self.output_directory, file_name)
        output = file(file_path, 'w')
        for entry in self.complete_transcript:
            output.write(self.format_transcript_entry(entry))
            output.write('\n\n')
        output.close()
