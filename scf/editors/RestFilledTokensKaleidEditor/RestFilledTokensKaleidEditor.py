from scf.editors.KaleidEditor import KaleidEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
import handlers


class RestFilledTimeTokenMakerKaleidEditor(KaleidEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.kaleids.RestFilledTimeTokenMaker,
        )
