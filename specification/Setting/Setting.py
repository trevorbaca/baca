from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, segment_name, context_name, scope, attribute_name, source, persistent):
        assert isinstance(segment_name, str) 
        assert isinstance(context_name, (str, type(None)))
        assert isinstance(attribute_name, str)
        assert isinstance(persistent, bool)
        assert isinstance(scope, (Scope, type(None)))
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_absolute(self):
        return not self.is_relative

    @property
    def is_relative(self):
        return isinstance(self.source, Selection)
