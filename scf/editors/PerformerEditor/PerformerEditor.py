from baca.scf.editors.InteractiveEditor import InteractiveEditor


class PerformerEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def InstrumentEditor(self):
        import baca
        return baca.scf.editors.InstrumentEditor

    @property
    def menu_title_contribution(self):
        if self.target is not None and self.target.name is not None:
            return self.target.name
        else:
            return 'performer'

    @property
    def summary_lines(self):
        if not self.target.instruments:
            result = '{}: (no instruments assigned)'.format(self.target.name)
        elif len(self.target.instruments) == 1 and self.target.name == \
            self.target.instruments[0].instrument_name:
            result = '{}'.format(self.target.name)
        else:
            instruments = ', '.join([x.instrument_name for x in self.target.instruments])
            result = '{} ({})'.format(self.target.name, instruments)
        result = [result]
        return result

    @property
    def target_class(self):
        from abjad.tools import scoretools
        return scoretools.Performer

    ### PUBLIC METHODS ###

    def add_instrument_interactively(self):
        '''Instrument if successfully added. Otherwise none.
        '''
        editor = self.InstrumentEditor(session=self.session)
        editor.conditionally_initialize_target()
        instrument = editor.target
        if instrument is not None:
            self.target.instruments.append(instrument)
            return instrument

    def delete_instrument_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('instrument number', 1, self.target.instrument_count)
        instrument_number = getter.run()
        if self.session.backtrack():
            return
        instrument_index = instrument_number - 1
        del(self.target.instruments[instrument_index])
    
    def edit_name_interactively(self):
        if self.target.name is None:
            spaced_variable_name = 'performer name'
        else:
            spaced_variable_name = 'new performer name'
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string(spaced_variable_name)
        name = getter.run()
        if self.session.backtrack():
            return
        self.target.name = name

    def handle_main_menu_response(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        if key == 'add':
            self.add_instrument_interactively()
        elif key == 'del':
            self.delete_instrument_interactively()
        elif key == 'mv':
            self.move_instrument_interactively()
        elif key in ('name', 'ren'):
            self.edit_name_interactively()
        elif key == 'rpn':
            return self.remove_name()
        else:
            self.edit_instrument_interactively(key)

    def edit_instrument_interactively(self, instrument_number):
        try:
            instrument_number = int(instrument_number)
        except:
            return
        if self.target.instrument_count < instrument_number:
            message = 'there is no instrument number {}'.format(instrument_number)
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        instrument_index = instrument_number - 1
        instrument = self.target.instruments[instrument_index]
        instrument_editor = self.InstrumentEditor(session=self.session, target=instrument)
        instrument_editor.run()

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        instrument_names = [x.instrument_name for x in self.target.instruments]
        menu_section.items_to_number = instrument_names
        menu_section.sentence_length_items.append(('add', 'add instrument'))
        if 0 < self.target.instrument_count:
            menu_section.sentence_length_items.append(('del', 'delete instrument'))
        if 1 < self.target.instrument_count:
            menu_section.sentence_length_items.append(('mv', 'move instrument'))
        if self.target.name is None:
            menu_section.sentence_length_items.append(('name', 'name performer'))
        else:
            menu_section.sentence_length_items.append(('ren', 'rename performer'))
            menu_section.sentence_length_items.append(('rpn', 'remove performer name'))
        return menu

    def move_instrument_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('old instrument number', 1, self.target.instrument_count)
        getter.append_integer_in_closed_range('new instrument number', 1, self.target.instrument_count)
        result = getter.run()
        if self.session.backtrack():
            return
        old_instrument_number, new_instrument_number = result
        old_instrument_index, new_instrument_index = old_instrument_number - 1, new_instrument_number - 1
        instrument = self.target.instruments[old_instrument_index]
        self.target.instruments.remove(instrument)
        self.target.instruments.insert(new_instrument_index, instrument)

    def remove_name(self):
        self.target.name = None
