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
            ('instrument_name', self.is_string, True, None),
            ('instrument_name_markup', self.is_markup, True, None), 
            ('short_instrument_name',  self.is_string, True, None),
            ('short_instrument_name_markup', self.is_markup, True, None),)
            
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
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name', result)

    def edit_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_markup('instrument name markup')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name_markup', result)

    def edit_pitch_range_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_pitch_range('pitch range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('pitch_range', result)
        
    def edit_short_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('short instrument name')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name', result)

    def edit_short_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_markup('short instrument name markup')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name_markup', result)
        
    def get_untuned_percussion_name_interactively(self):
        while True:
            self.append_breadcrumb('untuned percussion')
            menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
            section.menu_entry_tokens = instrumenttools.UntunedPercussion.known_untuned_percussion
            result = menu.run()
            if self.backtrack():
                self.pop_breadcrumb()
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                return result
        
    def handle_main_menu_result(self, result):
        if result == 'cl':
            self.print_not_implemented()
            #self.edit_clefs_interactively()
        elif result == 'in':
            self.edit_instrument_name_interactively()
        elif result == 'inm':
            self.edit_instrument_name_markup_interactively()
        elif result == 'pr':
            self.edit_pitch_range_interactively()
        elif result == 'sin':
            self.edit_short_instrument_name_interactively()
        elif result == 'sinm':
            self.edit_short_instrument_name_markup_interactively()
        elif result == 'tprd':
            if self.session.display_pitch_ranges_with_numbered_pitches:
                self.session.display_pitch_ranges_with_numbered_pitches = False
            else:
                self.session.display_pitch_ranges_with_numbered_pitches = True
        elif result == 'trans':
            self.print_not_implemented()
            #self.edit_transposition_interactively()

    def make_main_menu(self):
        #menu, section = self.make_new_menu(where=self.where(), is_keyed=False)
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tokens = self.target_attribute_menu_entry_tokens
        section = menu.make_new_section(is_keyed=False)
        if self.session.display_pitch_ranges_with_numbered_pitches:
            pitch_range_repr = self.target.pitch_range.one_line_numbered_chromatic_pitch_repr
        else:
            pitch_range_repr = self.target.pitch_range.one_line_named_chromatic_pitch_repr
        line = 'range: {}'.format(pitch_range_repr)
        section.append(('pr', line))
        clefs = [clef.clef_name for clef in self.target.all_clefs]
        clefs = ', '.join(clefs)
        line = 'clefs: {}'.format(clefs)
        section.append(('cl', line))
        if self.target.is_transposing:
            line = 'sounding pitch of fingered middle C: {}'
            line = line.format(self.target.sounding_pitch_of_fingered_middle_c.pitch_class_octave_label)
            section.append(('sp', line))
            line = 'interval of transposition: {}'
            line = line.format(self.target.interval_of_transposition)
            section.append(('int', line))
        section = menu.make_new_section(is_hidden=True)
        section.append(('tprd', 'toggle pitch range display'))
        return menu

    def select_instruments_from_instrumenttools_interactively(self):
        '''Return list of instruments or none.
        '''
        from abjad.tools import instrumenttools
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True, is_ranged=True)
        section.menu_entry_tokens = instrumenttools.list_instrument_names()
        while True:
            self.append_breadcrumb('select instrument')
            #print 'BEFORE: argument range is allowed: {!r}'.format(menu.argument_range_is_allowed)
            result = menu.run()
            #print 'ZOO: {!r}'.format(result)
            if self.backtrack():
                self.pop_breadcrumb()
                return    
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                break
        instrument_names = result
        this_result = []
        for instrument_name in instrument_names:
            instrument_name = instrument_name.title()
            instrument_name = instrument_name.replace(' ', '')
            exec('instrument = instrumenttools.{}()'.format(instrument_name))
            if isinstance(instrument, instrumenttools.UntunedPercussion):
                self.session.backtrack_preservation_is_active = True
                instrument_name = self.get_untuned_percussion_name_interactively()
                self.session.backtrack_preservation_is_active = False
                if self.backtrack():
                    continue
                instrument.instrument_name = instrument_name
            this_result.append(instrument)
        return this_result
