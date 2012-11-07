from abjad.tools import rhythmmakertools
from scf.editors.RhythmMakerEditor import RhythmMakerEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class TaleaFilledRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.TaleaFilledRhythmMaker,
        ('pattern', None, 'pa', getters.get_nonzero_integers, True),
        ('denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )
