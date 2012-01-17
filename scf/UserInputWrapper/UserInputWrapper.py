import collections


class UserInputWrapper(collections.OrderedDict):
    
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
        formatted_lines = []
        formatted_lines.append('user_input = {}(['.format(type(self).__name__))
        items = self.list_items
        for name, value in items[:-1]:
            line = '\t({!r}, {!r}),'.format(name, value)
            formatted_lines.append(line)
        formatted_lines.append('\t({!r}, {!r})])'.format(items[-1][0], items[-1][1]))
        return formatted_lines

    @property
    def is_complete(self):
        return bool(None not in self.itervalues())

    @property
    def is_empty(self):
        return all([x is None for x in self.itervalues()])

    @property
    def list_items(self):
        return list(self.iteritems())

    @property
    def values(self):
        return list(self.itervalues())

    ### PUBLIC METHODS ###

    def clear(self):
        for key in self:
            self[key] = None
