from abjad.tools import instrumenttools
from baca.scf.editors.InteractiveEditor import InteractiveEditor


# TODO: eventually make transposition information editable
# TODO: eventually make clef information editable
class InstrumentEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        if self.target is not None and self.target.instrument_name is not None:
            return self.target.instrument_name
        else:
            return 'instrument editor'

    @property
    def target_attribute_tuples(self):
        return (
            ('instrument_name', self.is_string, True),
            ('instrument_name_markup', self.is_markup, True), 
            ('short_instrument_name',  self.is_string, True),
            ('short_instrument_name_markup', self.is_markup, True),)
            
    @property
    def target_class(self):
        from abjad.tools.instrumenttools._Instrument import _Instrument
        return _Instrument

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            instruments = self.select_instruments_from_instrumenttools_interactively()
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None
    
    def edit_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('instrument name')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name', result)

    def edit_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_markup('instrument name markup')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name_markup', result)
        
    def edit_short_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('short instrument name')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name', result)

    def edit_short_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_markup('short instrument name markup')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name_markup', result)
        
    def get_untuned_percussion_name_interactively(self):
        self.breadcrumbs.append('untuned percussion')
        while True:
            menu, section = self.make_new_menu(where=self.where())
            menu.should_clear_terminal = False
            section.items_to_number = instrumenttools.UntunedPercussion.known_untuned_percussion
            key, value = menu.run()
            if self.session.backtrack():
                self.breadcrumbs.pop()
                return
            elif key is None:
                continue
            else:
                self.breadcrumbs.pop()
                return value
        
    def handle_main_menu_response(self, key, value):
        if key == 'cl':
            self.print_not_implemented()
            #self.edit_clefs_interactively()
        elif key == 'in':
            self.edit_instrument_name_interactively()
        elif key == 'inm':
            self.edit_instrument_name_markup_interactively()
        elif key == 'sin':
            self.edit_short_instrument_name_interactively()
        elif key == 'sinm':
            self.edit_short_instrument_name_markup_interactively()
        elif key == 'tprd':
            if self.session.display_pitch_ranges_with_numbered_pitches:
                self.session.display_pitch_ranges_with_numbered_pitches = False
            else:
                self.session.display_pitch_ranges_with_numbered_pitches = True
        elif key == 'trans':
            self.print_not_implemented()
            #self.edit_transposition_interactively()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.sentence_length_items = self.target_attribute_menu_entries
        section = menu.make_new_section()
        if self.session.display_pitch_ranges_with_numbered_pitches:
            pitch_range_repr = self.target.pitch_range.one_line_numbered_chromatic_pitch_repr
        else:
            pitch_range_repr = self.target.pitch_range.one_line_named_chromatic_pitch_repr
        line = 'range: {}'.format(pitch_range_repr)
        section.sentence_length_items.append(('tr', line))
        menu.hidden_items.append(('tprd', 'toggle pitch range display'))
        clefs = [clef.clef_name for clef in self.target.all_clefs]
        clefs = ', '.join(clefs)
        line = 'clefs: {}'.format(clefs)
        section.sentence_length_items.append(('cl', line))
        if self.target.is_transposing:
            line = 'sounding pitch of fingered middle C: {}'
            line = line.format(self.target.sounding_pitch_of_fingered_middle_c.pitch_class_octave_label)
            section.sentence_length_items.append(('sp', line))
            line = 'interval of transposition: {}'
            line = line.format(self.target.interval_of_transposition)
            section.sentence_length_items.append(('int', line))
        return menu

    def select_instruments_from_instrumenttools_interactively(self):
        '''Return list of instruments or none.
        '''
        from abjad.tools import instrumenttools
        self.breadcrumbs.append('select instrument')
        menu, section = self.make_new_menu(where=self.where())
        menu.allow_integer_range = True
        menu.should_clear_terminal = False
        section.items_to_number = instrumenttools.list_instrument_names()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.breadcrumbs.pop()
                return    
            elif key is None:
                continue
            else:
                self.breadcrumbs.pop()
                break
        instrument_names = value
        result = []
        for instrument_name in instrument_names:
            instrument_name = instrument_name.title()
            instrument_name = instrument_name.replace(' ', '')
            exec('instrument = instrumenttools.{}()'.format(instrument_name))
            if isinstance(instrument, instrumenttools.UntunedPercussion):
                self.session.backtrack_preservation_is_active = True
                instrument_name = self.get_untuned_percussion_name_interactively()
                self.session.backtrack_preservation_is_active = False
                if self.session.backtrack():
                    continue
                instrument.instrument_name = instrument_name
            result.append(instrument)
        return result
