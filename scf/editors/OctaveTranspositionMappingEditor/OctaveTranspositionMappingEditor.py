from abjad.tools import pitchtools
from scf.editors.ListEditor import ListEditor
from scf.editors.OctaveTranspositionMappingComponentEditor import OctaveTranspositionMappingComponentEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class OctaveTranspositionMappingEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = pitchtools.OctaveTranspositionMapping
    target_item_class = pitchtools.OctaveTranspositionMappingComponent
    target_item_creator_class = OctaveTranspositionMappingComponentEditor
    target_item_editor_class = OctaveTranspositionMappingComponentEditor
    target_item_identifier = 'octave transposition mapping component'
    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMapping,
        ('inventory_name', 'name', 'nm', getters.get_string),
        target_name_attribute='inventory_name',
        )
