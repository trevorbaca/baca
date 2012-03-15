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

    def store_settings(self, target_selection, value, is_persistent):
        if isinstance(target_selection, list):
            target_selections = target_selection
        else:
            target_selections = [target_selection]
        for target_selection in target_selections:
            setting = Setting(target_selection.context_name, scope=target_selection.scope)
            setting.store_value(value, is_persistent)
            self.settings.append(setting)
