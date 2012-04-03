from baca.specification.Selection import Selection


class Directive(object):

    ### INITIALIZER ###

    def __init__(self, target_selection, attribute_name, source, seed=None):
        self.target_selection = target_selection
        self.attribute_name = attribute_name
        self.source = source
        self.seed = seed

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_absolute(self):
        return not self.is_relative

    @property
    def is_relative(self):
        return isinstance(self.source, Selection)
