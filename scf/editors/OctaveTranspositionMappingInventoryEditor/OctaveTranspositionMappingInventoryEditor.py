from abjad.tools import pitchtools
from scf.editors.ListEditor import ListEditor
from scf.editors.OctaveTranspositionMappingEditor import OctaveTranspositionMappingEditor
from scf.menuing.UserInputGetter import UserInputGetter
#from scf import wizards


class OctaveTranspositionMappingInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = pitchtools.OctaveTranspositionMappingInventory
    #target_item_getter_configuration_method = OctaveTranspositionMappingEditor.run
    target_item_class = pitchtools.OctaveTranspositionMapping
    target_item_editor_class = OctaveTranspositionMappingEditor
    target_item_identifier = 'octave transposition mapping'
    target_items_identifier = 'octave transposition mappings'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    # TODO: maybe not necessary
    #@property
    #def target_summary_lines(self):
    #    result = []
    #    for item in self.target:
    #        result.append(repr(item))
    #    return result
