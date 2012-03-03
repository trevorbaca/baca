from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import kaleids


class PatternedTokensKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_class = kaleids.PatternedTokens
    target_manifest = TargetManifest(kaleids.PatternedTokens,
        ('pattern', 'pa', getters.get_nonzero_integers),
        ('denominator', 'de', getters.get_positive_integer_power_of_two),
        ('prolation_addenda', 'ad', getters.get_integers),
        ('secondary_divisions', 'sd', getters.get_integers),
        )

    ### PUBLIC METHODS ###

    def initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        for attribute_name in ('pattern', 'denominator'):
            if attribute_name in self.attributes_in_memory:
                args.append(self.attributes_in_memory.get(attribute_name))
        for attribute_name in ('prolation_addenda', 'secondary_divisions', 'pattern_helper',
            'prolation_addenda_helper', 'secondary_divisions_helper'):
            if attribute_name in self.attributes_in_memory:
                kwargs[attribute_name] = self.attributes_in_memory.get(attribute_name)
        try:
            self.target = self.target_class(*args, **kwargs)
        except TypeError:
            pass
