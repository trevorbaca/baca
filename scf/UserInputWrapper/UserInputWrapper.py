import collections


class UserInputWrapper(collections.OrderedDict):
    
    ### PUBLIC ATTRIBUTES ###

    @property
    def formatted_lines(self):
        formatted_lines = []
        formatted_lines.append('user_input = %s([' % type(self).__name__)
        for name, value in user_input_pairs[:-1]:
            line = '\t(%r, %r),' % (name, value)
            formatted_lines.append(line)
        formatted_lines.append('\t(%r, %r)])' % user_input_pairs[-1])
        return formatted_lines

    @property
    def is_complete(self):
        return bool(None not in self.itervalues())

    @property
    def items(self):
        return list(self.iteritems())

    @property
    def values(self):
        return list(self.itervalues())
