from baca.scf.editors.InteractiveEditor import InteractiveEditor


class InstrumentationSpecifierEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def menu_piece(self):
        return 'performers'

    @property
    def summary_lines(self):
        result = []
        for performer in self.target.performers:
            performer_editor = self.PerformerEditor(session=self.session, target=performer)
            result.extend(performer_editor.summary_lines)
        return result

    @property
    def target_class(self):
        from abjad.tools import scoretools
        return scoretools.InstrumentationSpecifier

    ### PUBLIC METHODS ###

    def add_performer_interactively(self):
        from abjad.tools import scoretools
        performer = scoretools.Performer()
        self.target.performers.append(performer)
        performer_editor = self.PerformerEditor(session=self.session, target=performer)
        instrument = performer_editor.add_instrument_interactively()
        performer.name = instrument.instrument_name
        return performer_editor

    def delete_performer_interactively(self):
        number = self.handle_raw_input('number')
        try:
            number = int(number)
        except:
            pass
        index = number - 1
        del(self.target.performers[index])

    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.target.performers[performer_index]
        except:
            performer = None
        return performer

    def handle_main_menu_response(self, key, value):
        if key is None:
            return True
        elif key == 'add':
            self.add_performer_interactively()
        elif key == 'b':
            return True
        elif key == 'del':
            self.delete_performer_interactively()
        elif key == 'mv':
            self.move_performer_interactively()
        else:
            try:
                performer_number = int(key)
            except:
                performer_number = None
            if performer_number is not None:
                performer = self.get_performer_from_performer_number(performer_number)
                performer_editor = self.PerformerEditor(session=self.session, target=performer)
                performer_editor.edit_interactively()

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu_section.items_to_number = self.summary_lines
        menu_section.sentence_length_items.append(('add', 'add performer'))
        menu_section.sentence_length_items.append(('del', 'delete performer'))
        menu_section.sentence_length_items.append(('mv', 'move performer up or down in list'))
        menu.menu_sections.append(menu_section)
        return menu

    def move_performer_interactively(self):
        old_number = self.handle_raw_input('old number')
        try:
            old_number = int(old_number)
        except:
            return
        old_index = old_number - 1
        performer = self.target.performers[old_index]
        new_number = self.handle_raw_input('new number')
        try:
            new_number = int(new_number)
        except:
            return
        new_index = new_number - 1
        self.target.performers.remove(performer)
        self.target.performers.insert(new_index, performer)
