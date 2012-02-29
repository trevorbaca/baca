import collections


class UserInputWrapper(collections.OrderedDict):
    
    def __init__(self, *arg):
        collections.OrderedDict.__init__(self, *arg)
        self._user_input_module_import_statements = []

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def editable_lines(self):
        pairs = list(self.iteritems())
        lines = []
        for pair in pairs:
            key, value = pair
            key = key.replace('_', ' ')
            if value is None:
                line = '{}: '.format(key)
            else:
                line = '{}: {!r}'.format(key, value)
            lines.append(line)
        return lines

    @property
    def formatted_lines(self):
        result = []
        items = self.list_items()
        if not items:
            result.append('user_input_wrapper = {}([])'.format(type(self).__name__))
        else:
            result.append('user_input_wrapper = {}(['.format(type(self).__name__))
            for name, value in items[:-1]:
                line = '\t({!r}, {!r}),'.format(name, value)
                result.append(line)
            result.append('\t({!r}, {!r})])'.format(items[-1][0], items[-1][1]))
        return result

    @property
    def is_complete(self):
        return bool(None not in self.itervalues())

    @property
    def is_empty(self):
        return all([x is None for x in self.itervalues()])

    @property
    def is_partially_complete(self):
        return not self.is_complete and not self.is_empty

    @property
    def user_input_module_import_statements(self):
        return self._user_input_module_import_statements

    ### PUBLIC METHODS ###

    def clear(self):
        for key in self:
            self[key] = None

    def list_items(self):
        return list(self.iteritems())

    def list_keys(self):
        return list(self.iterkeys())

    def list_values(self):
        return list(self.itervalues())
