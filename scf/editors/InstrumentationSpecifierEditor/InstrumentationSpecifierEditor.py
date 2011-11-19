from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentationSpecifierEditor(InteractiveEditor):

    def __init__(self, session=None, instrumentation=None):
        self.session = session
        self.instrumentation = instrumentation

    ### PUBLIC METHODS ###

    def add_instrument_to_performer_interactively(self, performer):
        instrument = self.select_instrument_from_instrumenttools_interactively()
        performer.instruments.append(instrument)
        return instrument
        
    def add_performer_to_instrumentation_interactively(self):
        from abjad.tools import scoretools
        performer = scoretools.Performer()
        self.instrumentation.performers.append(performer)
        instrument = self.add_instrument_to_performer_interactively(performer)
        performer.name = instrument.instrument_name

    def edit(self):
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        self.session.menu_pieces.append('instrumentation')
        self.instrumentation = self.instrumentation or scoretools.InstrumentationSpecifierEditor()
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            performer_number = None
            if key is None:
                pass
            elif key == 'b':
                break
            elif key == 'add':
                self.add_performer_to_instrumentation_interactively()
            elif key == 'mv':
                self.move_performer_interactively()
            else:
                try:
                    performer_number = int(key)
                except ValueError:
                    pass
            if performer_number is not None:
                performer = self.get_performer_from_performer_number(performer_number)
                self.edit_performer_interactively(performer)
        self.session.menu_pieces.pop()
        instrumentation = self.instrumentation
        self.instrumentation = None
        return instrumentation

    def edit_instrument_interactively(self, performer, instrument):
        self.session.menu_pieces.append(instrument.instrument_name)
        while True:
            menu = self.make_instrument_menu(performer, instrument)
            key, value = menu.run()
            if key == 'b':
                break
            elif key == 'del':
                performer.instruments.remove(instrument)
                break 
            elif key == 'mv':
                self.print_not_implemented()
        self.session.menu_pieces.pop()

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

    def edit_performer_interactively(self, performer):
        self.session.menu_pieces.append(performer.name)
        while True:
            menu = self.make_performer_menu(performer)
            key, value = menu.run()
            if key == 'b':
                break
            elif key == 'del':
                self.instrumentation.performers.remove(performer)
                break
            elif key == 'instr':
                self.edit_instruments_interactively(performer)
            elif key == 'mv':
                self.move_performer_interactively(performer)
            elif key == 'ren':
                self.name_performer_interactively(performer)
                break
            else:
                pass
        self.session.menu_pieces.pop()
        
    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.instrumentation.performers[performer_index]
        except:
            performer = None
        return performer

    def instrumentation_to_lines(self, instrumentation):
        result = []
        for performer in instrumentation.performers:
            summary = self.performer_to_one_line_summary(performer)
            result.append(summary)
        return result

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu_section.items_to_number = self.instrumentation_to_lines(self.instrumentation)
        menu_section.sentence_length_items.append(('add', 'add player'))
        menu_section.sentence_length_items.append(('mv', 'move player up or down in list'))
        menu.menu_sections.append(menu_section)
        return menu

    def make_instrument_menu(self, performer, instrument):
        menu = self.Menu(where=self.where(), session=self.session) 
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.menu_section_title = '{}: {}'.format(performer.name, instrument.instrument_name)
        menu_section.sentence_length_items.append(('del', 'delete performer instrument'))
        return menu

    def make_instruments_menu(self, performer):
        menu = self.Menu(where=self.where(), session=self.session) 
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.menu_section_title = 'instruments'
        instrument_names = [x.instrument_name for x in performer.instruments]
        menu_section.items_to_number = instrument_names
        menu_section.sentence_length_items.append(('add', 'add instrument'))
        return menu

    def make_performer_menu(self, performer):
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

    def move_performer_interactively(self):
        old_performer_number = raw_input('Old number> ')
        try:
            old_performer_number = int(old_performer_number)
        except:
            return
        old_performer_index = old_performer_number - 1
        performer = self.instrumentation.performers[old_performer_index]
        new_performer_number = raw_input('New number> ')
        try:
            new_performer_number = int(new_performer_number)
        except:
            return
        new_performer_index = new_performer_number - 1
        self.instrumentation.performers.remove(performer)
        self.instrumentation.performers.insert(new_performer_index, performer)

    def name_performer_interactively(self, performer):
        performer_name = raw_input('Performer name> ')
        print ''
        performer.name = performer_name
            
    def performer_to_one_line_summary(self, performer):
        if not performer.instruments:
            result = '{}: (no instruments assigned)'.format(performer.name)
        elif len(performer.instruments) == 1 and performer.name == \
            performer.instruments[0].instrument_name:
            result = '{}'.format(performer.name)
        else:
            instruments = ', '.join([x.instrument_name for x in performer.instruments])
            result = '{} ({})'.format(performer.name, instruments)
        return result

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
        exec('result = instrumenttools.{}()'.format(instrument_name))
        return result
