from abjad.tools.instrumenttools._Instrument import _Instrument
from abjad.tools import instrumenttools
from scf.editors.ClefMarkInventoryEditor import ClefMarkInventoryEditor
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters
from scf import selectors


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
    
    def handle_main_menu_result(self, result):
        if result == 'tprd':
            if self.session.display_pitch_ranges_with_numbered_pitches:
                self.session.display_pitch_ranges_with_numbered_pitches = False
            else:
                self.session.display_pitch_ranges_with_numbered_pitches = True
        else:
            InteractiveEditor.handle_main_menu_result(self, result)

    def make_main_menu(self):
        menu = InteractiveEditor.make_main_menu(self)
        hidden_section = menu.hidden_section
        hidden_section.append(('tprd', 'toggle pitch range display'))
        return menu

    # TODO: replace with instrument creation wizard
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
                selector = selectors.InstrumentToolsUntunedPercussionNameSelector(session=self.session)
                self.push_backtrack()
                instrument_name = selector.run()
                self.pop_backtrack()
                if self.backtrack():
                    continue
                instrument.instrument_name = instrument_name
            this_result.append(instrument)
        self.restore_breadcrumbs(cache=cache)
        return this_result
