from baca.scf.editors.ArticulationSpecifierEditor import ArticulationSpecifierEditor
from baca.scf.editors.ClefSpecifierEditor import ClefSpecifierEditor
from baca.scf.editors.DirectiveSpecifierEditor import DirectiveSpecifierEditor
from baca.scf.editors.DynamicSpecifierEditor import DynamicSpecifierEditor
from baca.scf.editors.InstrumentSpecifierEditor import InstrumentSpecifierEditor
from baca.scf.editors.NoteHeadSpecifierEditor import NoteHeadSpecifierEditor
from baca.scf.editors.OverrideSpecifierEditor import OverrideSpecifierEditor
from baca.scf.editors.PerformerSpecifierEditor import PerformerSpecifierEditor
from baca.scf.editors.PitchClassSpecifierEditor import PitchClassSpecifierEditor
from baca.scf.editors.RegistrationSpecifierEditor import RegistrationSpecifierEditor
from baca.scf.editors.RhythmSpecifierEditor import RhythmSpecifierEditor
from baca.scf.editors.StaffSpecifierEditor import StaffSpecifierEditor
from baca.scf.editors.TrillSpecifierEditor import TrillSpecifierEditor
from baca.scf.editors.TropingSpecifierEditor import TropingSpecifierEditor
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.TargetManifest import TargetManifest
from baca.scf.specifiers.PerformerContributionSpecifier import PerformerContributionSpecifier


class PerformerContributionSpecifierEditor(InteractiveEditor):

    target_class = PerformerContributionSpecifier
    target_manifest = TargetManifest(PerformerContributionSpecifier,
        ('articulation_specifier', 'art', ArticulationSpecifierEditor),
        ('clef_specifier', 'clf', ClefSpecifierEditor),
        ('directive_specifier', 'dir', DirectiveSpecifierEditor),
        ('dynamic_specifier', 'dyn', DynamicSpecifierEditor),
        ('instrument_specifier', 'ins', InstrumentSpecifierEditor),
        ('note_head_specifier', 'nhd', NoteHeadSpecifierEditor),
        ('override_specifier', 'ovr', OverrideSpecifierEditor),
        ('performer_specifier', 'per', PerformerSpecifierEditor),
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
        return self.target_name or 'performer contribution specifier editor'

    @property
    def target_name(self):
        if self.target is not None:
            if self.target.performer_specifier is not None:
                performer_name = self.target.performer_specifier.performer_name
                if performer_name:
                    return '{} contribution'.format(performer_name)
