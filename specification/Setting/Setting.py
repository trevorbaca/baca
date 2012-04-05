from abjad.tools.abctools.AbjadObject import AbjadObject


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, context_name, persistent=None, scope=None, temporary=None):
        self.context_name = context_name
        self.persistent = persistent
        self.scope = scope
        self.temporary = temporary

    ### PUBLIC METHODS ###

    def store_value(self, value, is_persistent):
        if is_persistent:
            self.persistent = value
        else:   
            self.temporary = value
