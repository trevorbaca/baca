from abjad.tools import timetokentools
from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class RestFilledTimeTokenMakerEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(timetokentools.RestFilledTimeTokenMaker,
        )
