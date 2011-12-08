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
    def menu_title_contribution(self):
        if self.target is not None and self.target.instrument_name is not None:
            return self.target.instrument_name
        else:
            return 'instrument editor'

    @property
    def target_attribute_menu_entries(self):
        result = []
        menu_keys = []
        target_attrs = ('instrument_name', 'instrument_name_markup', 
            'short_instrument_name', 'short_instrument_name_markup')
        for target_attr in target_attrs:
            menu_key = self.attribute_name_to_menu_key(target_attr, menu_keys)
            assert menu_key not in menu_keys
            menu_keys.append(menu_key)
            value = target_attr.replace('_', ' ')
            value = '{} ({!r})'.format(value, getattr(self.target, target_attr))
            pair = (menu_key, value)
            result.append(pair)
        return result
            
    @property
    def target_class(self):
        from abjad.tools.instrumenttools._Instrument import _Instrument
        return _Instrument

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            self.target = self.select_instrument_from_instrumenttools_interactively()
    
    def edit_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string('instrument name')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attr('instrument_name', result)

    def edit_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string('instrument name markup')
        result = getter.run()
        if self.session.backtrack():
            return
        exec('from abjad import *')
        exec('result = markuptools.Markup(result)')
        #self.conditionally_set_target_attr('instrument_name_markup', result)
        self.target.instrument_name_markup = result
        
    def edit_short_instrument_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string('short instrument name')
        result = getter.run()
        if self.session.backtrack():
            return
        self.conditionally_set_target_attr('short_instrument_name', result)

    def edit_short_instrument_name_markup_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string('short instrument name markup')
        result = getter.run()
        if self.session.backtrack():
            return
        exec('from abjad import *')
        exec('result = markuptools.Markup(result)')
        #self.conditionally_set_target_attr('short_instrument_name_markup', result)
        self.target.short_instrument_name_markup = result
        
    def handle_main_menu_response(self, key, value):
        #if key == 'b':
        #    return True
        #elif key == 'in':
        if key == 'in':
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
        menu_section.sentence_length_items = self.target_attribute_menu_entries
        return menu

    def select_instrument_from_instrumenttools_interactively(self):
        '''Return instrument or else none.
        '''
        from abjad.tools import instrumenttools
        self.session.menu_title_contributions.append('select instrument')
        menu = self.make_new_menu(where=self.where())
        menu.should_clear_terminal = False
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.items_to_number = instrumenttools.list_instrument_names()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.session.menu_title_contributions.pop()
                return    
            elif key is None:
                continue
            else:
                self.session.menu_title_contributions.pop()
                break
        instrument_name = value
        instrument_name = instrument_name.title()
        instrument_name = instrument_name.replace(' ', '')
        exec('result = instrumenttools.{}()'.format(instrument_name))
        return result
