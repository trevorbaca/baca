from abjad.tools import timetokentools
from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class OutputIncisedNoteFilledTimeTokenMakerEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(timetokentools.OutputIncisedNoteFilledTimeTokenMaker,
        ('prefix_signal', None, 'ps', getters.get_nonzero_integers, True),
        ('prefix_lengths', None, 'pl', getters.get_nonnegative_integers, True),
        ('suffix_signal', None, 'ss', getters.get_nonzero_integers, True),
        ('suffix_lengths', None, 'sl', getters.get_nonnegative_integers, True),
        ('denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        )
