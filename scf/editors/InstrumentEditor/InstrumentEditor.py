from abjad.tools.instrumenttools._Instrument import _Instrument
from abjad.tools import instrumenttools
from scf.editors.ClefMarkInventoryEditor import ClefMarkInventoryEditor
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class InstrumentEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_class = _Instrument
    target_manifest = TargetManifest(_Instrument,
        ('instrument_name', 'in', getters.get_string),
        ('instrument_name_markup', 'im', getters.get_markup),
        ('short_instrument_name',  'sn', getters.get_string),
        ('short_instrument_name_markup', 'sm', getters.get_markup),
        ('pitch_range', 'range', 'rg', getters.get_symbolic_pitch_range_string),
        ('all_clefs', 'clefs', 'cf', ClefMarkInventoryEditor),
        is_keyed=True, 
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.instrument_name

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            instruments = self.select_instruments_from_instrumenttools_interactively()
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None
    
    # TODO: remove in favor of target manifest
    def edit_instrument_name_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('instrument name')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name', result)

    # TODO: remove in favor of target manifest
    def edit_instrument_name_markup_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_markup('instrument name markup')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('instrument_name_markup', result)

    # TODO: remove in favor of target manifest
    def edit_pitch_range_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_pitch_range('pitch range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('pitch_range', result)
        
    # TODO: remove in favor of target manifest
    def edit_short_instrument_name_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('short instrument name')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name', result)

    # TODO: remove in favor of target manifest
    def edit_short_instrument_name_markup_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_markup('short instrument name markup')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('short_instrument_name_markup', result)
        
    # TODO: encapsulate in selector
    def get_untuned_percussion_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('untuned percussion')
            menu, section = self.make_menu(where=self.where(), is_numbered=True)
            section.tokens = instrumenttools.UntunedPercussion.known_untuned_percussion
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return result
        
#    # TODO: use baseclass method
#    def handle_main_menu_result(self, result):
#        if result == 'cl':
#            self.print_not_yet_implemented()
#        elif result == 'in':
#            self.edit_instrument_name_interactively()
#        elif result == 'im':
#            self.edit_instrument_name_markup_interactively()
#        elif result == 'pr':
#            self.edit_pitch_range_interactively()
#        elif result == 'sn':
#            self.edit_short_instrument_name_interactively()
#        elif result == 'sm':
#            self.edit_short_instrument_name_markup_interactively()
#        elif result == 'tprd':
#            if self.session.display_pitch_ranges_with_numbered_pitches:
#                self.session.display_pitch_ranges_with_numbered_pitches = False
#            else:
#                self.session.display_pitch_ranges_with_numbered_pitches = True
#        elif result == 'trans':
#            self.print_not_yet_implemented()

    def handle_main_menu_result(self, result):
        if result == 'tprd':
            if self.session.display_pitch_ranges_with_numbered_pitches:
                self.session.display_pitch_ranges_with_numbered_pitches = False
            else:
                self.session.display_pitch_ranges_with_numbered_pitches = True
        else:
            InteractiveEditor.handle_main_menu_result(self, result)

#    # TODO: use baseclass method
#    def make_main_menu(self):
#        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_keyed=True)
#        section.tokens = self.target_attribute_tokens
#        section.show_existing_values = True
#        section = menu.make_section(is_keyed=False)
#        if self.session.display_pitch_ranges_with_numbered_pitches:
#            pitch_range_repr = self.target.pitch_range.one_line_numbered_chromatic_pitch_repr
#        else:
#            pitch_range_repr = self.target.pitch_range.one_line_named_chromatic_pitch_repr
#        line = 'range: {}'.format(pitch_range_repr)
#        section.append(('pr', line))
#        clefs = [clef.clef_name for clef in self.target.all_clefs]
#        clefs = ', '.join(clefs)
#        line = 'clefs: {}'.format(clefs)
#        section.append(('cl', line))
#        if self.target.is_transposing:
#            line = 'sounding pitch of fingered middle C: {}'
#            line = line.format(self.target.sounding_pitch_of_fingered_middle_c.pitch_class_octave_label)
#            section.append(('sp', line))
#            line = 'interval of transposition: {}'
#            line = line.format(self.target.interval_of_transposition)
#            section.append(('int', line))
#        section = menu.make_section(is_hidden=True)
#        section.append(('tprd', 'toggle pitch range display'))
#        return menu

    def make_main_menu(self):
        menu = InteractiveEditor.make_main_menu(self)
        hidden_section = menu.hidden_section
        hidden_section.append(('tprd', 'toggle pitch range display'))
        return menu

    # TODO: encapsulate in selector
    def select_instruments_from_instrumenttools_interactively(self, clear=True, cache=False):
        '''Return list of instruments or none.'''
        from abjad.tools import instrumenttools
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_ranged=True)
        section.tokens = instrumenttools.list_instrument_names()
        while True:
            self.push_breadcrumb('select instrument')
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
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
            command = 'instrument = instrumenttools.{}()'.format(instrument_name)
            exec(command)
            if isinstance(instrument, instrumenttools.UntunedPercussion):
                self.push_backtrack()
                instrument_name = self.get_untuned_percussion_name_interactively()
                self.pop_backtrack()
                if self.backtrack():
                    continue
                instrument.instrument_name = instrument_name
            this_result.append(instrument)
        self.restore_breadcrumbs(cache=cache)
        return this_result
