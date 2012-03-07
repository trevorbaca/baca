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
