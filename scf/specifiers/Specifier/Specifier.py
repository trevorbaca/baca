from abc import ABCMeta
from abc import abstractproperty


class Specifier(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        variable_names = self.__init__.im_func.func_code.co_varnames[1:]
        self._variable_names = variable_names
        self.description = None

    ### OVERLOADS ###

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, type(self)):
            if self.variable_names == other.variable_names:
                for variable_name in self.variable_names:
                    if not getattr(self, variable_name) == getattr(other, variable_name):
                        return False
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        if self.variable_names:
            return '{}{!r}'.format(self.class_name, self.variable_names)
        else:
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
        result.append('{}('.format(self.importable_class_name))
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
    def importable_class_name(self):
        return 'specifiers.{}'.format(self.class_name)

    @abstractproperty
    def one_line_menuing_summary(self):
        pass

    @property
    def variable_names(self):
        return self._variable_names

    ### PUBLIC METHODS ###

    def get_format_pieces_of_expr(self, expr):
        if hasattr(expr, 'format_pieces'):
            return expr.format_pieces
        elif hasattr(expr, '_tools_package_qualified_repr'):
            return [expr._tools_package_qualified_repr]
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
