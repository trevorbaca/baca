class Session(object):
    
    def __init__(self, test=None, user_input=None):
        self._session_once_had_user_input = False
        self.initial_user_input = user_input
        self.menu_pieces = []
        self.scores_to_show = 'active'
        self.test = test
        self.test_result = None
        self.user_input = user_input
        self.user_specified_quit = False

    ### OVERLOADS ###

    def __bool__(self):
        return True

    def __repr__(self):
        summary = []
        if self.test is not None:
            summary.append('test={!r}'.format(self.test))
        if self.initial_user_input is not None:
            summary.append('initial_user_input={!r}'.format(self.initial_user_input))
        if self.user_input is not None:
            summary.append('user_input={!r}'.format(self.user_input))
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    def __str__(self):
        return '\n'.join(self.formatted_attributes)

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_displayable(self):
        return self.user_input is None and self.test is None

    @property
    def formatted_attributes(self):
        result = []
        result.append('initial_user_input: {!r}'.format(self.initial_user_input))
        result.append('menu_pieces: {!r}'.format(self.menu_pieces))
        result.append('scores_to_show: {!r}'.format(self.scores_to_show))
        result.append('test: {!r}'.format(self.test))
        result.append('test_result: {!r}'.format(self.test_result))
        result.append('user_input: {!r}'.format(self.user_input))
        return result

    @property
    def menu_header(self):
        if self.menu_pieces:
            return ' - '.join(self.menu_pieces)
        else:
            return ''

    @property
    def session_is_complete(self):
        return self.test_is_complete or self.user_input_is_consumed or self.user_specified_quit

    @property
    def session_once_had_user_input(self):
        return self._session_once_had_user_input

    @property
    def test_is_complete(self):
        if self.test is not None:
            if self.test_result is not None:
                return True
        return False

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

    def print_attributes(self):
        for attribute in self.formatted_attributes:
            print attribute
