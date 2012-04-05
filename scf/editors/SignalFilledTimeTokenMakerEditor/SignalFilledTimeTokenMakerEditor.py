from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import handlers


class SignalFilledTimeTokenMakerEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.kaleids.SignalFilledTimeTokenMaker,
        ('pattern', None, 'pa', getters.get_nonzero_integers, True),
        ('denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )
