from scf import getters
from scf import specifiers
from scf import wizards
#from scf.editors.ArticulationSpecifierEditor import ArticulationSpecifierEditor
#from scf.editors.ClefSpecifierEditor import ClefSpecifierEditor
#from scf.editors.DirectiveSpecifierEditor import DirectiveSpecifierEditor
#from scf.editors.DynamicSpecifierEditor import DynamicSpecifierEditor
#from scf.editors.InstrumentSpecifierEditor import InstrumentSpecifierEditor
#from scf.editors.NoteHeadSpecifierEditor import NoteHeadSpecifierEditor
#from scf.editors.OverrideSpecifierEditor import OverrideSpecifierEditor
#from scf.editors.PerformerSpecifierEditor import PerformerSpecifierEditor
#from scf.editors.PitchClassSpecifierEditor import PitchClassSpecifierEditor
#from scf.editors.RegistrationSpecifierEditor import RegistrationSpecifierEditor
#from scf.editors.RhythmSpecifierEditor import RhythmSpecifierEditor
#from scf.editors.StaffSpecifierEditor import StaffSpecifierEditor
#from scf.editors.TrillSpecifierEditor import TrillSpecifierEditor
#from scf.editors.TropingSpecifierEditor import TropingSpecifierEditor
#from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scf.editors.TargetManifest import TargetManifest
from scf.editors.get_parameter_specifier_editor import get_parameter_specifier_editor


#class MusicContributionSpecifierEditor(InteractiveEditor):
class MusicContributionSpecifierEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = specifiers.ParameterSpecifier
    item_creator_class = wizards.ParameterSpecifierCreationWizard
    item_editor_class = staticmethod(get_parameter_specifier_editor)
    item_identifier = 'parameter specifier'

    target_manifest = TargetManifest(specifiers.MusicContributionSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
#        (),
#        ('performer_specifier', 'per', PerformerSpecifierEditor),
#        ('instrument_specifier', 'str', InstrumentSpecifierEditor),
#        (),
#        ('rhythm_specifier', 'rhy', RhythmSpecifierEditor),
#        (),
#        ('pitch_class_specifier', 'pcs', PitchClassSpecifierEditor),
#        ('registration_specifier', 'reg', RegistrationSpecifierEditor),
#        ('troping_specifier', 'trp', TropingSpecifierEditor),
#        (),
#        ('dynamic_specifier', 'dyn', DynamicSpecifierEditor),
#        ('articulation_specifier', 'art', ArticulationSpecifierEditor),
#        ('note_head_specifier', 'nhd', NoteHeadSpecifierEditor),
#        (),
#        ('trill_specifier', 'trl', TrillSpecifierEditor),
#        ('override_specifier', 'ovr', OverrideSpecifierEditor),
#        ('directive_specifier', 'dir', DirectiveSpecifierEditor),
#        #(),
#        #('staff_specifier', 'stf', StaffSpecifierEditor),
#        #('clef_specifier', 'clf', ClefSpecifierEditor),

        target_attribute_name='name',
        )

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        if self.target:
            return self.target.one_line_menuing_summary
        return 'unknown contribution'

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class([])

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        kwargs = {}
        if menu_key == 'str':
            try:
                kwargs['instruments'] = \
                    self.target.performer_specifier.performer.instruments[:]
            except AttributeError:
                pass
        return kwargs
