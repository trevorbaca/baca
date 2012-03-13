from scf import getters
from scf.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scf.editors.TargetManifest import TargetManifest
import handlers


class NoteAndChordHairpinsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.dynamics.NoteAndChordHairpinsHandler,
        ('hairpin_tokens', None, 'ht', getters.get_hairpin_tokens, True),
        ('minimum_prolated_duration', None, 'md', getters.get_duration, True),
    )
