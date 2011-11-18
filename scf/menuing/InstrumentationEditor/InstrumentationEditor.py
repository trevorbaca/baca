from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    def __init__(self, session=None, instrumentation=None):
        self.session = session
        self.instrumentation = instrumentation

    ### PUBLIC METHODS ###

    def add_performer_to_instrumentation_interactively(self):
        from abjad.tools import scoretools
        designation = raw_input('Performer designation> ')
        print ''
        performer = scoretools.Performer(designation)
        while True:
            response = raw_input('Assign instrument to performer? ')
            print ''
            if response.lower() == 'y':
                instrument = self.select_instrument_interactively()
                performer.instruments.append(instrument)
            elif response.lower() == 'n':
                break
        self.instrumentation.performers.append(performer)

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
                performer_index = performer_number - 1
                self.manage_existing_performer_interactively(performer_index)
            #if self.session.session_is_complete:
            #    break 
        self.session.menu_pieces.pop()
        instrumentation = self.instrumentation
        self.instrumentation = None
        return instrumentation

    def instrumentation_to_lines(self, instrumentation):
        result = []
        for performer in instrumentation.performers:
            if not performer.instruments:
                result.append('{}: (none)'.format(performer.designation))
            else:
                instruments = ', '.join([x.instrument_name.contents_string for x in performer.instruments])
                result.append('{}: {}'.format(performer.designation, instruments))
        return result

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'performers'
        menu_section.items_to_number = self.instrumentation_to_lines(self.instrumentation)
        menu_section.sentence_length_items.append(('add', 'add performer'))
        menu.menu_sections.append(menu_section)
        return menu

    def manage_existing_performer_interactively(self, performer_index):
        self.print_not_implemented()

    def select_instrument_interactively(self):
        from abjad.tools import instrumenttools
        menu = self.Menu(where=self.where(), session=self.session)
        menu.should_clear_terminal = False
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'instruments'
        menu_section.items_to_number = instrumenttools.list_instrument_names()
        menu.menu_sections.append(menu_section)
        key, instrument_name = menu.run()
        # possibly return inside exec?
        exec('result = instrumenttools.{}()'.format(instrument_name))
        return result
