from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentationSpecifierEditor(InteractiveEditor):

    def __init__(self, session=None, instrumentation_specifier=None):
        InteractiveEditor.__init__(self, session=session)
        self.instrumentation_specifier = instrumentation_specifier

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def summary_lines(self):
        result = []
        for performer in self.instrumentation_specifier.performers:
            performer_editor = self.PerformerEditor(session=self.session, performer=performer)
            result.extend(performer_editor.summary_lines)
        return result

    ### PUBLIC METHODS ###

    def add_performer_interactively(self):
        from abjad.tools import scoretools
        performer = scoretools.Performer()
        self.instrumentation_specifier.performers.append(performer)
        performer_editor = self.PerformerEditor(session=self.session, performer=performer)
        instrument = performer_editor.add_instrument_interactively()
        performer.name = instrument.instrument_name
        return performer_editor

    def delete_performer_interactively(self):
        self.print_not_implemented()

    def edit_interactively(self):
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        self.session.menu_pieces.append('instrumentation_specifier')
        self.instrumentation_specifier = self.instrumentation_specifier or scoretools.InstrumentationSpecifier()
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            performer_number = None
            if key is None:
                pass
            elif key == 'add':
                self.add_performer_interactively()
            elif key == 'b':
                break
            elif key == 'del':
                self.delete_performer_interactively()
            elif key == 'mv':
                self.move_performer_interactively()
            else:
                try:
                    performer_number = int(key)
                except ValueError:
                    pass
            if performer_number is not None:
                performer = self.get_performer_from_performer_number(performer_number)
                #self.edit_performer_interactively(performer)
                performer_editor = self.PerformerEditor(session=self.session, performer=performer)
        self.session.menu_pieces.pop()
        instrumentation_specifier = self.instrumentation_specifier
        self.instrumentation_specifier = None
        return instrumentation_specifier

    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.instrumentation_specifier.performers[performer_index]
        except:
            performer = None
        return performer

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu_section.items_to_number = self.summary_lines
        menu_section.sentence_length_items.append(('add', 'add performer'))
        menu_section.sentence_length_items.append(('del', 'delete performer'))
        menu_section.sentence_length_items.append(('mv', 'move performer up or down in list'))
        menu.menu_sections.append(menu_section)
        return menu

    def move_performer_interactively(self):
        old_performer_number = raw_input('old number> ')
        try:
            old_performer_number = int(old_performer_number)
        except:
            return
        old_performer_index = old_performer_number - 1
        performer = self.instrumentation_specifier.performers[old_performer_index]
        new_performer_number = raw_input('new number> ')
        try:
            new_performer_number = int(new_performer_number)
        except:
            return
        new_performer_index = new_performer_number - 1
        self.instrumentation_specifier.performers.remove(performer)
        self.instrumentation_specifier.performers.insert(new_performer_index, performer)
