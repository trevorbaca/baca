import collections


class UserInputWrapper(collections.OrderedDict):
    
    ### PUBLIC ATTRIBUTES ###

    @property
    def is_complete(self):
        return bool(None not in self.itervalues())
