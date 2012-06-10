from scf import getters
from scf.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scf.editors.TargetManifest import TargetManifest
import handlertools


class NoteAndChordHairpinHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.dynamics.NoteAndChordHairpinHandler,
        ('hairpin_token', None, 'ht', getters.get_hairpin_token, True),
        ('minimum_prolated_duration', None, 'md', getters.get_duration, True),
    )
