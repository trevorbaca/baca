from scf import getters
from scf.editors.ArticulationHandlerEditor import ArticulationHandlerEditor
from scf.editors.TargetManifest import TargetManifest
import handlers



class ReiteratedArticulationHandlerEditor(ArticulationHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlers.articulations.ReiteratedArticulationHandler,
        ('articulation_list', None, 'al', getters.get_articulations, False),
        ('minimum_prolated_duration', None, 'nd', getters.get_duration, False),
        ('maximum_prolated_duration', None, 'xd', getters.get_duration, False),
        ('minimum_written_pitch', None, 'np', getters.get_named_chromatic_pitch, False),
        ('maximum_written_pitch', None, 'xp', getters.get_named_chromatic_pitch, False),
        )
