from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import kaleids


class NoteFilledTokensKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_class = kaleids.NoteFilledTokens
    target_manifest = TargetManifest(kaleids.NoteFilledTokens,
        )
