from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import kaleids


class PatternedTokensKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_class = kaleids.PatternedTokens
    target_manifest = TargetManifest(kaleids.PatternedTokens,
        ('pattern', None, 'pa', getters.get_nonzero_integers, True),
        ('denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )

    ### PUBLIC METHODS ###

    def initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        #for attribute_name in ('pattern', 'denominator'):
        for attribute_name in self.target_mandatory_attribute_names:
            if attribute_name in self.attributes_in_memory:
                args.append(self.attributes_in_memory.get(attribute_name))
        #for attribute_name in ('prolation_addenda', 'secondary_divisions', 'pattern_helper',
        #    'prolation_addenda_helper', 'secondary_divisions_helper'):
        for attribute_name in self.target_keyword_attribute_names:
            if attribute_name in self.attributes_in_memory:
                kwargs[attribute_name] = self.attributes_in_memory.get(attribute_name)
        try:
            self.target = self.target_class(*args, **kwargs)
        except TypeError:
            pass
