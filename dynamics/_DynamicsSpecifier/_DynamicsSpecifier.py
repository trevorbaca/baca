from abjad.tools import durationtools
from fractions import Fraction


class _DynamicsSpecifier(object):
    '''Dynamics specifier.
    '''

    def __init__(self, minimum_prolated_duration = None):
        self.minimum_prolated_duration = minimum_prolated_duration

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % (type(self).__name__)

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def minimum_prolated_duration():
        def fget(self):
            return self._minimum_prolated_duration
        def fset(self, minimum_prolated_duration):
            if minimum_prolated_duration is None:
                self._minimum_prolated_duration = minimum_prolated_duration
            else:
                duration = durationtools.duration_token_to_duration_pair(minimum_prolated_duration)
                self._minimum_prolated_duration = Fraction(*duration)

    ### PUBLIC METHODS ###

    @staticmethod
    def is_hairpin_token(arg):
        from abjad.tools import contexttools
        from abjad.tools import spannertools
        if isinstance(arg, tuple) and \
            len(arg) == 3 and \
            (not arg[0] or contexttools.DynamicMark.is_dynamic_name(arg[0])) and \
            spannertools.HairpinSpanner.is_hairpin_shape_string(arg[1]) and \
            (not arg[2] or contexttools.DynamicMark.is_dynamic_name(arg[2])):
            if arg[0] and arg[2]:
                start_ordinal = contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal(arg[0])
                stop_ordinal = contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal(arg[2])
                if arg[1] == '<':
                    return start_ordinal < stop_ordinal
                else:
                    return stop_ordinal < start_ordinal
            else:
                return True
        else:
            return False
