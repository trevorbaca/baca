from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentEditor(InteractiveEditor):

    ### OVERLOADS ###

    def __repr__(self):
        if self.target is None:
            summary = ''
        else:
            summary = 'target={!r}'.format(self.target)
        return '{}({})'.format(type(self).__name__, summary)

    ### PUBLIC ATTRIBUTES ###

    @property
    def menu_piece(self):
        if self.target is not None:
            return self.target.instrument_name
        else:
            return 'instrument'

    @property
    def target_class(self):
        from abjad.tools.instrumenttools._Instrument import _Instrument
        return _Instrument

    ### PUBLIC METHODS ###

    def edit_instrument_name_interactively(self):
        instrument_name = raw_input('instrument name> ')
        assert isinstance(instrument_name, (str))
        self.target.instrument_name = instrument_name

    def edit_instrument_name_markup_interactively(self):
        instrument_name_markup = raw_input('instrument name markup> ')
        exec('instrument_name_markup = Markup(instrument_name_markup)')
        self.target.instrument_name_markup = instrument_name_markup
        
    def edit_short_instrument_name_interactively(self):
        short_instrument_name = raw_input('short instrument name> ')
        assert isinstance(short_instrument_name, (str))
        self.target.short_instrument_name = short_instrument_name

    def edit_short_instrument_name_markup_interactively(self):
        short_instrument_name_markup = raw_input('short instrument name markup> ')
        exec('short_instrument_name_markup = Markup(short_instrument_name_markup)')
        self.target.short_instrument_name_markup = short_instrument_name_markup
        
    def handle_main_menu_response(self, key, value):
        '''True when calling function should break.
        '''
        if key == 'b':
            return True
        elif key == 'in':
            self.edit_instrument_name_interactively()
        elif key == 'inm':
            self.edit_instrument_name_markup_interactively()
        elif key == 'sin':
            self.edit_short_instrument_name_interactively()
        elif key == 'sinm':
            self.edit_short_instrument_name_markup_interactively()

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.sentence_length_items.append(('in', 'instrument name'))
        menu_section.sentence_length_items.append(('inm', 'instrument name markup'))
        menu_section.sentence_length_items.append(('sin', 'short instrument name'))
        menu_section.sentence_length_items.append(('sinm', 'short instrument name markup'))
        return menu
