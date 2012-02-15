from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.TargetManifest import TargetManifest
from baca.scf.specifiers.PerformerContributionSpecifier import PerformerContributionSpecifier


class PerformerContributionSpecifierEditor(InteractiveEditor):

    target_class = PerformerContributionSpecifier
#    target_manifest = TargetManifest(PerformerContributionSpecifier,
#        ('articulation_indicator', 'art', ArticulationIndicatorEditor),
#        ('clef_indicator', 'clf', ClefIndicatorEditor),
#        ('directive_indicator', 'dir', DirectiveIndicatorEditor),
#        ('dynamic_indicator', 'dyn', DynamicIndicatorEditor),
#        ('instrument_indicator', 'ins', InstrumentIndicatorEditor),
#        ('note_head_indicator', 'nhd', NoteHeadIndicatorEditor),
#        ('override_indicator', 'ovr', OverrideIndicatorEditor),
#        ('performer_indicator', 'per', PerformerIndicatorEditor),
#        ('pitch_class_indicator', 'pcs', PitchClassIndicatorEditor),
#        ('registration_indicator', 'reg', RegistrationIndicatorEditor),
#        ('rhythm_indicator', 'rhy', RhythmIndicatorEditor),
#        ('staff_indicator', 'stf', StaffIndicatorEditor),
#        ('trill_indicator', 'trl', TrillIndicatorEditor),
#        ('troping_indicator', 'trp', TropingIndicatorEditor),
#        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'performer contribution specifier editor'

    @property
    def target_name(self):
        if self.target is not None:
            if self.target.performer_indicator is not None:
                performer_name = self.target.performer_indicator.performer_name
                if performer_name:
                    return '{} contribution'.format(performer_name)
