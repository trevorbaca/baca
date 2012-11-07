from abjad.tools import rhythmmakertools
from scf.editors.RhythmMakerEditor import RhythmMakerEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class RestFilledRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.RestFilledRhythmMaker,
        )
