from abjad.tools.abctools.AbjadObject import AbjadObject


class InterpretationSetting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, persistent=None, temporary=None):
        self.persistent = persistent
        self.temporary = temporary

    ### PUBLIC METHODS ###

    def store_value(self, value, is_persistent):
        if is_persistent:
            self.persistent = value
        else:   
            self.temporary = value
