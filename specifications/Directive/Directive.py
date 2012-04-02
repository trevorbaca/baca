class Directive(object):

    ### INITIALIZER ###

    def __init__(self, selection, handler, seed=None):
        self.selection = selection
        self.handler = handler
        self.seed = seed
