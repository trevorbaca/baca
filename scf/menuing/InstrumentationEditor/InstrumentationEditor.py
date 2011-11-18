from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    def __init__(self, session=None, instrumentation=None):
        self.session = session
        self.instrumentation = instrumentation

    ### PUBLIC METHODS ###

    def add_performer_to_instrumentation_interactively(self):
        from abjad.tools import scoretools
        performer = scoretools.Performer()
        self.instrumentation.performers.append(performer)
        instrument = self.select_instrument_from_instrumenttools_interactively()
        performer.instruments.append(instrument)
        performer.name = instrument.instrument_name.contents_string

    def edit(self):
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        self.session.menu_pieces.append('edit instrumentation')
        self.instrumentation = self.instrumentation or scoretools.InstrumentationSpecifier()
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
            else:
                try:
                    performer_number = int(key)
                except ValueError:
                    pass
            if performer_number is not None:
                performer = self.get_performer_from_performer_number(performer_number)
                self.edit_performer_interactively(performer)
            #if self.session.session_is_complete:
            #    break 
        self.session.menu_pieces.pop()
        instrumentation = self.instrumentation
        self.instrumentation = None
        return instrumentation

    def edit_performer_instruments_interactively(self, performer):
        self.print_not_implemented()

    def edit_performer_interactively(self, performer):
        self.session.menu_pieces.append('performers')
        while True:
            menu = self.make_edit_performer_menu(performer)
            key, value = menu.run()
            if key == 'b':
                break
            elif key == 'del':
                self.instrumentation.performers.remove(performer)
                break
            elif key == 'instr':
                self.edit_performer_instruments_interactively(performer)
            elif key == 'mv':
                self.move_performer_interactively(performer)
            elif key == 'name':
                self.name_performer_interactively(performer)
            else:
                pass
            #if self.session.session_is_complete:
            #    break
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
        menu_section.menu_section_title = 'performers'
        menu_section.items_to_number = self.instrumentation_to_lines(self.instrumentation)
        menu_section.sentence_length_items.append(('add', 'add performer'))
        menu.menu_sections.append(menu_section)
        return menu

    def make_edit_performer_menu(self, performer):
        menu = self.Menu(where=self.where(), session=self.session) 
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.menu_section_title = self.performer_to_one_line_summary(performer)
        menu_section.sentence_length_items.append(('del', 'delete performer'))
        menu_section.sentence_length_items.append(('instr', "edit performer instruments"))
        menu_section.sentence_length_items.append(('mv', 'move performer up or down'))
        menu_section.sentence_length_items.append(('name', '(re)name performer'))
        return menu

    def move_performer_interactively(self, performer):
        self.print_not_implemented()

    def name_performer_interactively(self, performer):
        performer_name = raw_input('Performer name> ')
        print ''
        performer.name = performer_name
            
    def performer_to_one_line_summary(self, performer):
        if not performer.instruments:
            result = '{}: (no instruments assigned)'.format(performer.name)
        elif len(performer.instruments) == 1 and performer.name == \
            performer.instruments[0].instrument_name.contents_string:
            result = '{}'.format(performer.name)
        else:
            instruments = ', '.join([x.instrument_name.contents_string for x in performer.instruments])
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
