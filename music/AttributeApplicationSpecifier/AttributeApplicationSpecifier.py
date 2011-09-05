from baca.music.InstrumentAttributeApplicationSpecifier import \
    InstrumentAttributeApplicationSpecifier


class AttributeApplicationSpecifier(object):
    '''Class to encapsulate all settings necessary
    to pass to a method or function that applies
    some set of attributes to some chunk of score.
    '''

    #def __init__(self, attribute_name, instrument_names, proportions = None):
    def __init__(self, instrument_names, proportions = None):
        #self.attribute_name = attribute_name
        self.instrument_names = instrument_names
        self.proportions = proportions
        self.default = InstrumentAttributeApplicationSpecifier(self.proportions)
        self._init_instrument_attribute_application_specifiers()

    ### OVERLOADS ###

    ### PRIVATE METHODS ###

    def _init_instrument_attribute_application_specifiers(self):
        for instrument_name in self.instrument_names:
            #specifier = InstrumentAttributeApplicationSpecifier(instrument_name, self.proportions)
            specifier = InstrumentAttributeApplicationSpecifier(self.proportions)
            setattr(self, instrument_name, specifier)
