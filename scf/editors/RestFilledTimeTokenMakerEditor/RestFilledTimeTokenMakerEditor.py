from abjad.tools import timetokentools
from scf.editors.TimeTokenMakerEditor import TimeTokenMakerEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class RestFilledTimeTokenMakerEditor(TimeTokenMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(timetokentools.RestFilledTimeTokenMaker,
        )
