from abjad.tools import instrumenttools
from baca.scf.editors.InteractiveEditor import InteractiveEditor


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
        if key == 'in':
            self.edit_instrument_name_interactively()
        elif key == 'inm':
            self.edit_instrument_name_markup_interactively()
        elif key == 'sin':
            self.edit_short_instrument_name_interactively()
        elif key == 'sinm':
            self.edit_short_instrument_name_markup_interactively()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.sentence_length_items = self.target_attribute_menu_entries
        section = self.MenuSection()
        line = 'traditional range: {}'.format(self.target.traditional_range)
        section.sentence_length_items.append(('tr', line))
        #menu.sections.append(section)
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
