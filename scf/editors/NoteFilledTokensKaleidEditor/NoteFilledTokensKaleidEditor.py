from scf import getters
from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
import handlers


class NoteFilledTokensKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.kaleids.NoteFilledTokens,
        )
