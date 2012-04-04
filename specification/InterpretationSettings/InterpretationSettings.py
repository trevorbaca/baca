from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.InterpretationSetting import InterpretationSetting


class InterpretationSettings(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, aggregate=None, articulations=None, dynamics=None,
        pitch_classes=None, register=None, tempo=None, transform=None):
        self.aggregate = aggregate or InterpretationSetting()
        self.articulations = articulations or InterpretationSetting()
        self.dynamics = dynamics or InterpretationSetting()
        self.pitch_classes = pitch_classes or InterpretationSetting()
        self.register = register or InterpretationSetting()
        self.tempo = tempo or InterpretationSetting()
        self.transform = transform or InterpretationSetting()

    ### PUBLIC METHODS ###

    def remove_temporary_settings(self):
        for keyword_argument_name in self._keyword_argument_names:
            setting = getattr(self, keyword_argument_name)
            setting.temporary = None
