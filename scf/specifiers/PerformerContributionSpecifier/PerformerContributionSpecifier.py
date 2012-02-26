from scf.specifiers.Specifier import Specifier


class PerformerContributionSpecifier(Specifier):

    def __init__(self,
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
        Specifier.__init__(self)
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

    ### OVERLOADS ###

    def __repr__(self):
        if self.performer_specifier:
            return '{}({!r})'.format(self.class_name, self.performer_specifier)
        else:
            return '{}()'.format(self.class_name)

    ### READ-ONLY ATTRIBUTES ###

    @property
    def one_line_menuing_summary(self):
        return '{}: {}'.format(self.performer_label, self.parameter_summary_string)

    @property
    def parameter_summary_string(self):
        parameter_specifiers = []
        for variable_name in self.variable_names:
            variable_value = getattr(self, variable_name)
            if variable_value:
                parameter_specifiers.append(repr(variable_value))
        if len(parameter_specifiers) == 1:
            return '1 parameter specified'
        elif 1 < len(parameter_specifiers):
            return '{} parameterspecified'.format(len(parameter_specifiers))
        else:
            return 'no parameters specified'

    @property
    def performer_label(self):
        try:
            return self.performer_specifier.performer.name
        except AttributeError:
            return 'unknown performer'

