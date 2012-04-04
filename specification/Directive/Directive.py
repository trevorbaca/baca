from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Selection import Selection


class Directive(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, target_selection, attribute_name, source, is_persistent=True, seed=None):
        self.target_selection = target_selection
        self.attribute_name = attribute_name
        self.source = source
        self.is_persistent = is_persistent
        self.seed = seed

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_absolute(self):
        return not self.is_relative

    @property
    def is_relative(self):
        return isinstance(self.source, Selection)
