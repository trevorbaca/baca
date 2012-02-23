class Specifier(object):

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### READ-ONLY ATTRIBUTES ###

    @property
    def class_name(self):
        return type(self).__name__

    @property
    def format(self):
        return '\n'.join(self.format_pieces)

    @property
    def format_pieces(self):
        result = []
        result.append('{}('.format(type(self).__name__))
        for variable_name in sorted(self.variable_names):
            variable_value = getattr(self, variable_name)
            if variable_value is not None:
                format_pieces = self.get_format_pieces_of_expr(variable_value)
                format_pieces = self.indent_format_pieces(variable_name, format_pieces)
                result.extend(format_pieces)
        result.append('\t)')
        return result

    @property
    def human_readable_class_name(self):
        return iotools.uppercamelcase_to_space_delimited_lowercase(self.class_name)

    @property
    def variable_names(self):
        return self.__init__.im_func.func_code.co_varnames[1:]

    ### PUBLIC METHODS ###

    def get_format_pieces_of_expr(self, expr):
        if hasattr(expr, 'format_pieces'):
            return expr.format_pieces
        else:
            return [repr(expr)]

    def indent_format_pieces(self, name, format_pieces):
        result = []
        if len(format_pieces) == 1:
            result.append('\t{}={},'.format(name, format_pieces[0]))
        elif 1 < len(format_pieces):
            result.append('\t{}={}'.format(name, format_pieces[0]))
            for format_piece in format_pieces[1:-1]:
                result.append('\t' + format_piece)
            result.append('\t' + format_pieces[-1] + ',') 
        return result
