class Session(object):
    
    def __init__(self, menu_pieces=None, scores_to_show='active', test=None, user_input=None):
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
    def test_is_complete(self):
        if self.test is not None:
            if self.test_result is not None:
                return True
        return False
    
    ### PUBLIC METHODS ###

    def print_attributes(self):
        for attribute in self.formatted_attributes:
            print attribute
