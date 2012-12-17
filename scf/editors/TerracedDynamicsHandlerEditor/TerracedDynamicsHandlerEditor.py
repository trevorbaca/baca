from experimental.tools import handlertools
from scf import getters
from scf.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scf.editors.TargetManifest import TargetManifest


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.dynamics.TerracedDynamicsHandler,
        ('dynamics', None, 'dy', getters.get_dynamics, True),
        ('minimum_prolated_duration', None, 'md', getters.get_duration, True),
    )
