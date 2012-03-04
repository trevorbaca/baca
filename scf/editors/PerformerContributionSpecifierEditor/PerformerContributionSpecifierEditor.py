from scf import specifiers
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


class PerformerContributionSpecifierEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(specifiers.PerformerContributionSpecifier,
        ('performer_specifier', 'per', PerformerSpecifierEditor),
        ('instrument_specifier', 'str', InstrumentSpecifierEditor),
        (),
        ('rhythm_specifier', 'rhy', RhythmSpecifierEditor),
        (),
        ('pitch_class_specifier', 'pcs', PitchClassSpecifierEditor),
        ('registration_specifier', 'reg', RegistrationSpecifierEditor),
        ('troping_specifier', 'trp', TropingSpecifierEditor),
        (),
        ('dynamic_specifier', 'dyn', DynamicSpecifierEditor),
        ('articulation_specifier', 'art', ArticulationSpecifierEditor),
        ('note_head_specifier', 'nhd', NoteHeadSpecifierEditor),
        (),
        ('trill_specifier', 'trl', TrillSpecifierEditor),
        ('override_specifier', 'ovr', OverrideSpecifierEditor),
        ('directive_specifier', 'dir', DirectiveSpecifierEditor),
        #(),
        #('staff_specifier', 'stf', StaffSpecifierEditor),
        #('clef_specifier', 'clf', ClefSpecifierEditor),
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'unknown performer'

    @property
    def target_name(self):
        try:
            return self.target.performer_specifier.performer.name
        except AttributeError:
            return

    ### PUBLIC METHODS ###

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        kwargs = {}
        if menu_key == 'str':
            try:
                kwargs['instruments'] = \
                    self.target.performer_specifier.performer.instruments[:]
            except AttributeError:
                pass
        return kwargs
