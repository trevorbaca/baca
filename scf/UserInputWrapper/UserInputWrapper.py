import collections


class UserInputWrapper(collections.OrderedDict):
    
    ### PUBLIC ATTRIBUTES ###

    @property
    def editable_lines(self):
        pairs = list(self.iteritems())
        lines = []
        for pair in pairs:
            key, value = pair
            key = key.replace('_', ' ')
            if value is None:
                line = '%s: ' % key
            else:
                line = '%s: %r' % (key, value)
            lines.append(line)
        return lines

    @property
    def formatted_lines(self):
        formatted_lines = []
        formatted_lines.append('user_input = %s([' % type(self).__name__)
        items = self.items
        for name, value in items[:-1]:
            line = '\t(%r, %r),' % (name, value)
            formatted_lines.append(line)
        formatted_lines.append('\t(%r, %r)])' % items[-1])
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
