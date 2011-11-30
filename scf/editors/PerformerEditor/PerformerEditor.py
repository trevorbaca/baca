from baca.scf.editors.InteractiveEditor import InteractiveEditor


class PerformerEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def InstrumentEditor(self):
        import baca
        return baca.scf.editors.InstrumentEditor

    @property
    def menu_piece(self):
        if self.target is not None:
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
        instrument_editor = self.InstrumentEditor()
        instrument_editor.conditionally_initialize_target()
        instrument = instrument_editor.target
        self.target.instruments.append(instrument)
        return instrument

    def delete_instrument_interactively(self):
        number = self.handle_raw_input('number')
        try:
            number = int(number)
        except:
            pass
        index = number - 1
        del(self.target.instruments[index])
    
    def edit_name_interactively(self):
        name = self.handle_raw_input('name')
        self.target.name = name

    def handle_main_menu_response(self, key, value):
        if key == 'b':
            #return True
            return 'back'
        elif key == 'db':
            return self.add_instrument_interactively()
        elif key == 'del':
            return self.delete_instrument_interactively()
        elif key == 'mv':
            return self.move_instrument_interactively()
        elif key in ('name', 'ren'):
            self.edit_name_interactively()
            return True # maybe eliminate this line?
        elif key == 'un':
            return self.unname()
        else:
            try:
                instrument_number = int(key)
                instrument_index = instrument_number - 1
                instrument = self.target.instruments[instrument_index]
            except:
                instrument = None
            if instrument is not None:
                instrument_editor = self.InstrumentEditor(session=self.session, target=instrument)
                return instrument_editor.edit_interactively()

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        instrument_names = [x.instrument_name for x in self.target.instruments]
        menu_section.items_to_number = instrument_names
        menu_section.sentence_length_items.append(('del', 'delete instrument'))
        if self.target.is_doubling:
            value = 'add or remove instrument'
        else:
            value = 'add instrument'
        menu_section.sentence_length_items.append(('inst', value))
        if 1 < self.target.instrument_count:
            menu_section.sentence_length_items.append(('mv', 'move instrument up or down in list'))
        if self.target.name is None:
            menu_section.sentence_length_items.append(('name', 'name'))
        else:
            menu_section.sentence_length_items.append(('ren', 'rename performer'))
            menu_section.sentence_length_items.append(('un', 'unname performer'))
        return menu

    def move_instrument_interactively(self):
        old_number = self.handle_raw_input('old number')
        try:
            old_number = int(old_number)
        except:
            return
        old_index = old_number - 1
        instrument = self.target.instruments[old_index]
        new_number = self.handle_raw_input('new number')
        try:
            new_number = int(new_number)
        except:
            return
        new_index = new_number - 1
        self.target.instruments.remove(instrument)
        self.target.instruments.insert(new_index, instrument)

    def unname(self):
        self.target.name = None
