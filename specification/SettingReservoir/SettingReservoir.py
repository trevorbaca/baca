from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Setting import Setting


class SettingReservoir(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, dummy_score, settings=None):
        self.dummy_score = dummy_score
        self.settings = settings or []

    ### PUBLIC METHODS ###

    def get_setting(self, context_name):
        for setting in self.settings:
            pass
