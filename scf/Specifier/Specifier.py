class Specifier(object):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def attribute_format_pieces(self):
        result = []
        for co_name in self.__init__.im_func.func_code.co_names:
            value = getattr(self, co_name)
            if value is not None:
                format_pieces = self.get_format_pieces_of_expr(value)
                format_pieces = self.indent_format_pieces(co_name, format_pieces)
                result.extend(format_pieces)
        return result

    @property
    def format(self):
        return '\n'.join(self.format_pieces)

    @property
    def format_pieces(self):
        result = []
        result.append('{}('.format(type(self).__name__))
        for attribute_format_piece in self.attribute_format_pieces:
            result.append('\t' + attribute_format_piece + ',')
        result.append('\t' + ')')
        return result

    ### PUBLIC METHODS ###

    def get_format_pieces_of_expr(self, expr):
        if hasattr(expr, 'format_pieces'):
            return expr.format_pieces
        elif isinstance(expr, list):
            result = []
            result.append('[')
            for element in expr:
                format_pieces = self.get_format_pieces_of_expr(element)
                format_pieces = self.indent_format_pieces(format_pieces)
                for format_piece in format_pieces:
                    result.append('\t' + format_piece + ',')
            result.append(']')
        else:
            return [repr(expr)]

    def indent_format_pieces(self, format_pieces, name=None):
        result = []
        if len(format_pieces) == 1:
            if name is not None:
                result.append('{}={}'.format(name, format_pieces[0]))
            else:
                result.append('{}'.format(format_pieces[0]))
        elif 1 < len(format_pieces):
            if name is not None:
                result.append('{}={}'.format(name, format_pieces[0]))
                for format_piece in format_pieces[1:]:
                    result.append('\t' + format_piece)
            else:
                result.append('{}'.format(format_pieces[0]))
                for format_piece in format_pieces[1:]:
                    result.append('\t' + format_piece)
        return result
