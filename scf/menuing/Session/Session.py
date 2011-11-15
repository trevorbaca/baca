class Session(object):
    
    def __init__(self, menu_pieces=None, hide_mothballed_scores=True, test=None, user_input=None):
        if menu_pieces is None:
            self.menu_pieces = []
        else:
            self.menu_pieces = menu_pieces 
        self.hide_mothballed_scores = hide_mothballed_scores
        self.test = test
        self.user_input = user_input

    ### OVERLOADS ###

    def __bool__(self):
        return True

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### PUBLIC ATTRIBUTES ###

    @property
    def menu_header(self):
        if self.menu_pieces:
            return self.menu_pieces[-1]
