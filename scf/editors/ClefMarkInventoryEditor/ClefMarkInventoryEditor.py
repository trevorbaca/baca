from abjad.tools import contexttools
from scf.editors.ClefMarkEditor import ClefMarkEditor
from scf.editors.ListEditor import ListEditor
from scf.editors.TargetManifest import TargetManifest
from scf.editors.TempoMarkEditor import TempoMarkEditor
from scf.menuing.UserInputGetter import UserInputGetter


class ClefMarkInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = contexttools.ClefMarkInventory
    target_item_getter_configuration_method = UserInputGetter.append_clef
    target_item_class = contexttools.ClefMark
    target_item_editor_class = ClefMarkEditor
    target_item_identifier = 'clef mark'
    target_manifest = TargetManifest(contexttools.ClefMarkInventory,
        target_name_attribute='inventory_name',
        )
