from baca.specification.Selection import Selection


class Directive(object):

    ### INITIALIZER ###

    def __init__(self, target_selection, attribute_name, source, seed=None):
        self.target_selection = target_selection
        self.attribute_name = attribute_name
        self.source = source
        self.seed = seed

    ### SPECIAL METHODS ###

    def __repr__(self):
        mandatory_arguments = [self.target_selection, self.attribute_name, self.source]
        mandatory_arguments = ', '.join([repr(x) for x in mandatory_arguments])
        if self.seed is not None:
            return '{}({}, seed={!r})'.format(type(self).__name__, mandatory_arguments, self.seed)
        else:
            return '{}({})'.format(type(self).__name__, mandatory_arguments)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_absolute(self):
        return not self.is_relative

    @property
    def is_relative(self):
        return isinstance(self.source, Selection)
