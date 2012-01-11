class ScoreTemplate(object):

    def __init__(self, spaced_name=None):
        self.spaced_name = spaced_name

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def spaced_name():
        def fget(self):
            return self._spaced_name
        def fset(self, spaced_name):
            self._spaced_name = spaced_name
        return property(**locals())
        
    ### PUBLIC METHODS ###

    def make_empty_score(self):
        pass
