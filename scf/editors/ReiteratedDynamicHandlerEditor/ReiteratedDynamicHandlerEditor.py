from scf import getters
from scf.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scf.editors.TargetManifest import TargetManifest
import handlers


class ReiteratedDynamicHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.dynamics.ReiteratedDynamicHandler,
        ('dynamic_name', None, 'dy', getters.get_dynamic, True),
        ('minimum_prolated_duration', None, 'md', getters.get_duration, True),
    )
