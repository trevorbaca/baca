from abc import ABCMeta
from abc import abstractproperty
from abjad.tools import iotools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Specifier(AbjadObject):
    
    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    def __init__(self, description=None, name=None):
        self.description = description
        self.name = name

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, type(self)):
            if self._mandatory_argument_values == other._mandatory_argument_values:
                if self._keyword_argument_name_value_strings == other._keyword_argument_name_value_strings:
                    return True
        return False

#    ### PRIVATE READ-ONLY PROPERTIES ###
#
#    @property
#    def _keyword_argument_names(self):
#        '''Defined by hand so that this tuple is inheritable by subclasses. 
#        Is there a way to derive this programmatically *and* be inheritable by subclasses?
#        '''
#        return tuple(sorted([
#            'description',
#            'name',
#            ]))

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def format(self):
        return self._tools_package_qualified_indented_repr

    @property
    def human_readable_class_name(self):
        return iotools.uppercamelcase_to_space_delimited_lowercase(self.class_name)

    @abstractproperty
    def one_line_menuing_summary(self):
        pass
