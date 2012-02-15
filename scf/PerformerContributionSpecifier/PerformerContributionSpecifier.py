class PerformerContributionSpecifier(object):

    def __init__(self,
        articulation_indicator=None,
        clef_indicator=None,
        directive_indicator=None,
        dynamic_indicator=None,
        instrument_indicator=None,
        note_head_indicator=None,
        override_spanner_indicator=None,
        pitch_class_indicator=None,
        registration_indicator=None,
        rhythm_indicator=None,
        staff_indicator=None,
        trill_indicator=None,
        troping_indicator=None,
        ):
        self.articulation_indicator = articulation_indicator
        self.clef_indicator = clef_indicator
        self.directive_indicator = directive_indicator
        self.dynamic_indicator = dynamic_indicator
        self.instrument_indicator = instrument_indicator
        self.note_head_indicator = note_head_indicator
        self.override_spanner_indicator = override_spanner_indicator
        self.pitch_class_indicator = pitch_class_indicator
        self.registration_indicator = registration_indicator
        self.rhythm_indicator = rhythm_indicator
        self.staff_indicator = staff_indicator
        self.trill_indicator = trill_indicator
        self.troping_indicator=troping_indicator
        
    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def format_pieces(self):
        result = []
        return result
