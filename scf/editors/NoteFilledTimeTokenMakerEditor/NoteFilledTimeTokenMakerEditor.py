from abjad.tools import timetokentools
from scf import getters
from scf.editors.TimeTokenMakerEditor import TimeTokenMakerEditor
from scf.editors.TargetManifest import TargetManifest


class NoteFilledTimeTokenMakerEditor(TimeTokenMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(timetokentools.NoteFilledTimeTokenMaker,
        )
