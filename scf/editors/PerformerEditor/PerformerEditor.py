from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class PerformerEditor(InteractiveEditor):

    def __init__(self, session=None, performer=None):
        InteractiveEditor.__init__(self, session=session)
        self.performer = performer

    ### PUBLIC ATTRIBUTES ###

    @property
    def InstrumentEditor(self):
        import baca
        return baca.scf.editors.InstrumentEditor

    @property
    def summary_lines(self):
        if not self.performer.instruments:
            result = '{}: (no instruments assigned)'.format(self.performer.name)
        elif len(self.performer.instruments) == 1 and self.performer.name == \
            self.performer.instruments[0].instrument_name:
            result = '{}'.format(self.performer.name)
        else:
            instruments = ', '.join([x.instrument_name for x in self.performer.instruments])
            result = '{} ({})'.format(self.performer.name, instruments)
        result = [result]
        return result

    ### PUBLIC METHODS ###

    def add_instrument_interactively(self):
        instrument = self.select_instrument_from_instrumenttools_interactively()
        self.performer.instruments.append(instrument)
        return instrument

    def delete_instrument_interactively(self):
        self.print_not_implemented()
    
    def edit_instruments_interactively(self, performer):
        self.session.menu_pieces.append('instruments')
        while True:
            menu = self.make_instruments_menu(performer)
            key, value = menu.run()
            if key == 'b':
                break
            elif key == 'add':
                self.add_instrument_to_performer_interactively(performer)
            else:
                try:
                    instrument_number = int(key)
                    instrument_index = instrument_number - 1
                    instrument = performer.instruments[instrument_index]
                except:
                    instrument = None
                if instrument is not None:
                    self.edit_instrument_interactively(performer, instrument)
        self.session.menu_pieces.pop()

    def edit_interactively(self):
        self.session.menu_pieces.append(performer.name)
        while True:
            menu = self.make_main_menu(performer)
            key, value = menu.run()
            if key == 'b':
                break
            elif key == 'db':
                self.edit_instruments_interactively(performer)
            elif key == 'mv':
                self.move_performer_interactively(performer)
            elif key == 'ren':
                self.name_performer_interactively(performer)
                break
            else:
                pass
        self.session.menu_pieces.pop()

    def make_instruments_menu(self, performer):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        instrument_names = [x.instrument_name for x in performer.instruments]
        menu_section.items_to_number = instrument_names
        menu_section.sentence_length_items.append(('add', 'add instrument'))
        return menu
    
    def make_main_menu(self, performer):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.sentence_length_items.append(('del', 'delete'))
        if performer.is_doubling:
            value = 'add or remove doubling'
        else:
            value = 'add doubling'
        menu_section.sentence_length_items.append(('db', value))
        menu_section.sentence_length_items.append(('ren', 'rename'))
        return menu

    def name_performer_interactively(self, performer):
        performer_name = raw_input('performer name> ')
        print ''
        performer.name = performer_name

    def select_instrument_from_instrumenttools_interactively(self):
        from abjad.tools import instrumenttools
        menu = self.Menu(where=self.where(), session=self.session)
        menu.should_clear_terminal = False
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'instruments'
        menu_section.items_to_number = instrumenttools.list_instrument_names()
        menu.menu_sections.append(menu_section)
        key, instrument_name = menu.run()
        instrument_name = instrument_name.replace(' ', '')
        exec('result = instrumenttools.{}()'.format(instrument_name.capitalize()))
        return result
