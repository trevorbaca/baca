from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Selection import Selection
from baca.specification.Setting import Setting


class Directive(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, target_selection, attribute_name, source, persistent=True):
        self.target_selection = target_selection
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent

    ### PUBLIC METHODS ###

    def make_setting_with_context_name(self, context_name):
        args = []
        args.extend([self.target_selection.segment_name, context_name, self.target_selection.scope])
        args.extend([self.attribute_name, self.source, self.persistent])
        return Setting(*args)

    def unpack(self):
        assert isinstance(self.target_selection.context_names, (list, type(None)))
        settings = []
        if self.target_selection.context_names in (None, []):
            settings.append(self.make_setting_with_context_name(None))
        else:
            for context_name in self.target_selection.context_names:
                settings.append(self.make_setting_with_context_name(context_name))
        return settings
