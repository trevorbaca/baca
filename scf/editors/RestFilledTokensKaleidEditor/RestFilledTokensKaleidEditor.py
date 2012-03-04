from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import kaleids


class RestFilledTokensKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_class = kaleids.RestFilledTokens
    target_manifest = TargetManifest(kaleids.RestFilledTokens,
        )
