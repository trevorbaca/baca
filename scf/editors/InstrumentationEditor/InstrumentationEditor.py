from abjad.tools import scoretools
from scf import getters
from scf import wizards
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerEditor import PerformerEditor
from scf.editors.TargetManifest import TargetManifest


class InstrumentationEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = scoretools.Performer
    target_item_creator_class = wizards.PerformerCreationWizard
    target_item_creator_class_kwargs = {'is_ranged': True}
    target_item_editor_class = PerformerEditor
    target_item_identifier = 'performer'
    target_manifest = TargetManifest(scoretools.InstrumentationSpecifier,
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'performers'

    @property
    def target_items(self):
        return self.target.performers
