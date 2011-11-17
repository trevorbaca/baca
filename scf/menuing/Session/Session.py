class Session(object):
    
    def __init__(self, menu_pieces=None, scores_to_show='active', test=None, user_input=None):
        self._session_once_had_user_input = False
        if menu_pieces is None:
            self.menu_pieces = []
        else:
            self.menu_pieces = menu_pieces 
        self.scores_to_show = scores_to_show
        self.test = test
        self.test_result = None
        self.user_input = user_input

    ### OVERLOADS ###

    def __bool__(self):
        return True

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    def __str__(self):
        return '\n'.join(self.formatted_attributes)

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_displayable(self):
        return self.user_input is None and self.test is None

    @property
    def menu_header(self):
        if self.menu_pieces:
            return self.menu_pieces[-1]

    @property
    def formatted_attributes(self):
        result = []
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
    def test_is_complete(self):
        if self.test is not None:
            if self.test_result is not None:
                return True
        return False

    @property
    def session_is_complete(self):
        return self.test_is_complete or self.user_input_is_consumed

    @property
    def session_once_had_user_input(self):
        return self._session_once_had_user_input

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
        #return bool(self.user_input == '')
        #return self.user_input in (None, '')
        return self.user_input is None
    
    ### PUBLIC METHODS ###

    def print_attributes(self):
        for attribute in self.formatted_attributes:
            print attribute
