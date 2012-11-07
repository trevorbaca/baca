from abjad.tools import rhythmmakertools
from scf import getters
from scf.editors.RhythmMakerEditor import RhythmMakerEditor
from scf.editors.TargetManifest import TargetManifest


class NoteFilledRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.NoteFilledRhythmMaker,
        )
