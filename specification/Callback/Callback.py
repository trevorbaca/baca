from abjad.tools.abctools.AbjadObject import AbjadObject


class Callback(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, callback, string):
        self.callback = callback
        self.string = string

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        return self.callback(expr)
