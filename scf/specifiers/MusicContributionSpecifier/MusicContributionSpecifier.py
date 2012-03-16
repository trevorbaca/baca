from scf.specifiers.Specifier import Specifier


class MusicContributionSpecifier(Specifier):

    def __init__(self,
        name=None,
        description=None,
        articulation_specifier=None,
        clef_specifier=None,
        directive_specifier=None,
        dynamic_specifier=None,
        instrument_specifier=None,
        note_head_specifier=None,
        override_specifier=None,
        performer_specifier=None,
        pitch_class_specifier=None,
        registration_specifier=None,
        rhythm_specifier=None,
        staff_specifier=None,
        trill_specifier=None,
        troping_specifier=None,
        ):
        Specifier.__init__(self, description=description, name=name)
        self.articulation_specifier = articulation_specifier
        self.clef_specifier = clef_specifier
        self.directive_specifier = directive_specifier
        self.dynamic_specifier = dynamic_specifier
        self.instrument_specifier = instrument_specifier
        self.note_head_specifier = note_head_specifier
        self.override_specifier = override_specifier
        self.performer_specifier = performer_specifier
        self.pitch_class_specifier = pitch_class_specifier
        self.registration_specifier = registration_specifier
        self.rhythm_specifier = rhythm_specifier
        self.staff_specifier = staff_specifier
        self.trill_specifier = trill_specifier
        self.troping_specifier=troping_specifier

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or 'unknown contribution'
