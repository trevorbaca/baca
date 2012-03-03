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
