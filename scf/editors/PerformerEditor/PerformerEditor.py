from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._Instrument import _Instrument
from scf import getters
from scf import wizards
from scf.editors.ListEditor import ListEditor
from scf.editors.InstrumentEditor import InstrumentEditor
from scf.editors.TargetManifest import TargetManifest


class PerformerEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = _Instrument
    target_item_creator_class = wizards.InstrumentCreationWizard
    target_item_creator_class_kwargs = {'is_ranged': True}
    target_item_editor_class = InstrumentEditor
    target_item_identifier = 'instrument'
    target_manifest = TargetManifest(scoretools.Performer,
        ('name', 'nm', getters.get_string),
        target_attribute_name='name',
        )
    
    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_items(self):
        return self.target.instruments 
