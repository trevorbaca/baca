from scf.editors.ArticulationSpecifierEditor import ArticulationSpecifierEditor
from scf.editors.ClefSpecifierEditor import ClefSpecifierEditor
from scf.editors.DirectiveSpecifierEditor import DirectiveSpecifierEditor
from scf.editors.DynamicSpecifierEditor import DynamicSpecifierEditor
from scf.editors.InstrumentSpecifierEditor import InstrumentSpecifierEditor
from scf.editors.NoteHeadSpecifierEditor import NoteHeadSpecifierEditor
from scf.editors.OverrideSpecifierEditor import OverrideSpecifierEditor
from scf.editors.PerformerSpecifierEditor import PerformerSpecifierEditor
from scf.editors.PitchClassSpecifierEditor import PitchClassSpecifierEditor
from scf.editors.RegistrationSpecifierEditor import RegistrationSpecifierEditor
from scf.editors.RhythmSpecifierEditor import RhythmSpecifierEditor
from scf.editors.StaffSpecifierEditor import StaffSpecifierEditor
from scf.editors.TrillSpecifierEditor import TrillSpecifierEditor
from scf.editors.TropingSpecifierEditor import TropingSpecifierEditor
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.PerformerContributionSpecifier import PerformerContributionSpecifier


class PerformerContributionSpecifierEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_class = PerformerContributionSpecifier
    target_manifest = TargetManifest(PerformerContributionSpecifier,
        ('performer_specifier', 'per', PerformerSpecifierEditor),
        ('articulation_specifier', 'art', ArticulationSpecifierEditor),
        ('clef_specifier', 'clf', ClefSpecifierEditor),
        ('directive_specifier', 'dir', DirectiveSpecifierEditor),
        ('dynamic_specifier', 'dyn', DynamicSpecifierEditor),
        ('instrument_specifier', 'ins', InstrumentSpecifierEditor),
        ('note_head_specifier', 'nhd', NoteHeadSpecifierEditor),
        ('override_specifier', 'ovr', OverrideSpecifierEditor),
        ('pitch_class_specifier', 'pcs', PitchClassSpecifierEditor),
        ('registration_specifier', 'reg', RegistrationSpecifierEditor),
        ('rhythm_specifier', 'rhy', RhythmSpecifierEditor),
        ('staff_specifier', 'stf', StaffSpecifierEditor),
        ('trill_specifier', 'trl', TrillSpecifierEditor),
        ('troping_specifier', 'trp', TropingSpecifierEditor),
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'unknown performer'

    @property
    def target_name(self):
        try:
            return self.target.performer_specifier.performer.name
        except AttributeError:
            return
