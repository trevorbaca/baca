from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import kaleids


class PartForcedPatternedTokensKaleidEditor(KaleidEditor):

	### CLASS ATTRIBTUES ###

    target_class = kaleids.PartForcedPatternedTokens
    target_manifest = TargetManifest(kaleids.PartForcedPatternedTokens,
        ('pattern', 'pa', getters.get_nonzero_integers),
        ('denominator', 'de', getters.get_positive_integer_power_of_two),
        ('prolation_addenda', 'ad', getters.get_integers),
        ('lefts', 'lf',  getters.get_integers),
        ('middles', 'mi', getters.get_integers),
        ('rights', 'rt', getters.get_integers),
        ('left_lengths', 'll', getters.get_positive_integers),
        ('right_lengths', 'rl', getters.get_positive_integers),
        ('secondary_divisions', 'sd', getters.get_integers),
        )

    ### PUBLIC METHODS ###

    def initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        for attribute_name in ('pattern', 'denominator'):
            if attribute_name in self.attributes_in_memory:
                args.append(self.attributes_in_memory.get(attribute_name))
        for attribute_name in (
            'prolation_addenda', 
            'lefts', 
            'middles', 
            'rights', 
            'left_lengths', 
            'right_lengths',
            'pattern_helper',
            'prolation_addenda_helper',
            'lefts_helper',
            'middles_helper',
            'rights_helper',
            'left_lengths_helper',
            'right_lengths_helper', 
            'secondary_divisions_helper',
            ):
            if attribute_name in self.attributes_in_memory:
                kwargs[attribute_name] = self.attributes_in_memory.get(attribute_name)
        try:
            self.target = self.target_class(*args, **kwargs)
        except TypeError:
            pass
