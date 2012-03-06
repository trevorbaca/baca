from abjad.tools import pitchtools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class OctaveTranspositionMappingComponentEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_class = pitchtools.OctaveTranspositionMappingComponent
    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMappingComponent,
        ('source_pitch_range', 'pr', getters.get_symbolic_pitch_range_string),
        ('target_octave_start_pitch', 'sp', getters.get_integer),
        )

    ### PUBLIC METHODS ##

    def conditionally_initialize_target(self):
        pass

    def initialize_target_from_attributes_in_memory(self):
        initializer_token = []
        for attribute_name in ('source_pitch_range', 'target_octave_start_pitch'):
            if attribute_name in self.attributes_in_memory:
                initializer_token.append(self.attributes_in_memory.get(attribute_name))
        initializer_token = tuple(initializer_token)
        self.target = self.target_class(*initializer_token)
