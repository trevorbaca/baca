from abjad.tools import timetokentools
from scf import getters
from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest


class NoteFilledTimeTokenMakerEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(timetokentools.NoteFilledTimeTokenMaker,
        )
