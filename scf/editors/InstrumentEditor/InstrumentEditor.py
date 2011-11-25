from baca.scf.editors.InteractiveEditor import InteractiveEditor


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

    def conditionally_initialize_target(self):
        self.target = self.target or self.select_instrument_from_instrumenttools_interactively()
    
    def edit_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('instrument name')
        getter.tests.append(self.is_string)
        getter.helps.append('must be string.')
        result = getter.run()
        self.conditionally_set_target_attr('instrument_name', result)

    def edit_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('instrument name markup')
        getter.tests.append(self.is_string)
        getter.helps.append('must be string.')
        result = getter.run()
        exec('from abjad import *')
        exec('result = markuptools.Markup(result)')
        #self.conditionally_set_target_attr('instrument_name_markup', result)
        self.target.instrument_name_markup = result
        
    def edit_short_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('short instrument name')
        getter.tests.append(self.is_string)
        getter.helps.append('must be string.')
        result = getter.run()
        self.conditionally_set_target_attr('short_instrument_name', result)

    def edit_short_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('short instrument name markup')
        getter.tests.append(self.is_string)
        getter.helps.append('must be string.')
        result = getter.run()
        exec('from abjad import *')
        exec('result = markuptools.Markup(result)')
        #self.conditionally_set_target_attr('short_instrument_name_markup', result)
        self.target.short_instrument_name_markup = result
        
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
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.sentence_length_items.append(('in', 'instrument name'))
        menu_section.sentence_length_items.append(('inm', 'instrument name markup'))
        menu_section.sentence_length_items.append(('sin', 'short instrument name'))
        menu_section.sentence_length_items.append(('sinm', 'short instrument name markup'))
        return menu

    def select_instrument_from_instrumenttools_interactively(self):
        from abjad.tools import instrumenttools
        self.session.menu_pieces.append('select instrument')
        menu = self.make_new_menu(where=self.where())
        menu.should_clear_terminal = False
        menu_section = self.MenuSection()
        menu_section.items_to_number = instrumenttools.list_instrument_names()
        menu.menu_sections.append(menu_section)
        key, instrument_name = menu.run()
        instrument_name = instrument_name.replace(' ', '')
        exec('result = instrumenttools.{}()'.format(instrument_name.capitalize()))
        self.session.menu_pieces.pop()
        return result
