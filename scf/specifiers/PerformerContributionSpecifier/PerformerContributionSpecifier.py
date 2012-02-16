from baca.scf.specifiers.Specifier import Specifier


class PerformerContributionSpecifier(Specifier):

    def __init__(self,
        articulation_specifier=None,
        clef_specifier=None,
        directive_specifier=None,
        dynamic_specifier=None,
        instrument_specifier=None,
        note_head_specifier=None,
        override_spanner_specifier=None,
        performer_specifier=None,
        pitch_class_specifier=None,
        registration_specifier=None,
        rhythm_specifier=None,
        staff_specifier=None,
        trill_specifier=None,
        troping_specifier=None,
        ):
        self.articulation_specifier = articulation_specifier
        self.clef_specifier = clef_specifier
        self.directive_specifier = directive_specifier
        self.dynamic_specifier = dynamic_specifier
        self.instrument_specifier = instrument_specifier
        self.note_head_specifier = note_head_specifier
        self.override_spanner_specifier = override_spanner_specifier
        self.performer_specifier = performer_specifier
        self.pitch_class_specifier = pitch_class_specifier
        self.registration_specifier = registration_specifier
        self.rhythm_specifier = rhythm_specifier
        self.staff_specifier = staff_specifier
        self.trill_specifier = trill_specifier
        self.troping_specifier=troping_specifier
