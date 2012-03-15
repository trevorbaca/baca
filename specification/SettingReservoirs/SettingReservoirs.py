from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.SettingReservoir import SettingReservoir
import collections


class SettingReservoirs(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, dummy_score, aggregate=None, articulations=None, dynamics=None,
        pitch_classes=None, register=None, tempo=None, time_signatures=None, transform=None):
        self.dummy_score = dummy_score
        self.aggregate = aggregate or self.make_setting_reservoir()
        self.articulations = articulations or self.make_setting_reservoir()
        self.dynamics = dynamics or self.make_setting_reservoir()
        self.pitch_classes = pitch_classes or self.make_setting_reservoir()
        self.register = register or self.make_setting_reservoir()
        self.tempo = tempo or self.make_setting_reservoir()
        self.time_signatures = time_signatures or self.make_setting_reservoir()
        self.transform = transform or self.make_setting_reservoir()

    ### PUBLIC METHODS ###

#    def initialize_contexts(self):
#        for context in contexttools.iterate_contexts_forward_in_expr(self.score):
#            assert context.context_name is not None
#            self.contexts[context_name] = context

    def make_setting_reservoir(self):
        return SettingReservoir(self.dummy_score)

    def remove_temporary_settings(self):
        for keyword_argument_name in self._keyword_argument_names:
            setting = getattr(self, keyword_argument_name)
            setting.temporary = None
