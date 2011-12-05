from baca.scf.editors.InteractiveEditor import InteractiveEditor


class InstrumentationSpecifierEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def menu_piece(self):
        return 'performers & instrumentation'

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

#    def add_performer_interactively(self):
#        from abjad.tools import scoretools
#        performer = scoretools.Performer()
#        self.target.performers.append(performer)
#        performer_editor = self.PerformerEditor(session=self.session, target=performer)
#        instrument = performer_editor.add_instrument_interactively()
#        performer.name = instrument.instrument_name

    def add_performer_interactively(self):
        from abjad.tools import scoretools
        performer_name = self.select_performer_name_interactively()
        if self.session.backtrack():
            return
        elif performer_name:
            performer = scoretools.Performer(performer_name)
            self.target.performers.append(performer)
            return performer

    def delete_performer_interactively(self):
        number = self.handle_raw_input('performer number')
        try:
            number = int(number)
        except:
            pass
        if self.target.performer_count < number:
            message = 'there is no performer number {}.'.format(number)
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        index = number - 1
        del(self.target.performers[index])

    def edit_performer_interactively(self, performer_number):
        try:
            performer_number = int(performer_number)
        except:
            return
        performer = self.get_performer_from_performer_number(performer_number)
        performer_editor = self.PerformerEditor(session=self.session, target=performer)
        performer_editor.edit_interactively()

    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.target.performers[performer_index]
        except:
            performer = None
        return performer

    def handle_main_menu_response(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        if key == 'add':
            self.add_performer_interactively()
        elif key == 'del':
            self.delete_performer_interactively()
        elif key == 'mv':
            self.move_performer_interactively()
        else:
            self.edit_performer_interactively(key)

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.items_to_number = self.summary_lines
        menu_section.sentence_length_items.append(('add', 'add performer'))
        menu_section.sentence_length_items.append(('del', 'delete performer'))
        menu_section.sentence_length_items.append(('mv', 'move performer'))
        return menu

    def move_performer_interactively(self):
        old_number = self.handle_raw_input('old number')
        try:
            old_number = int(old_number)
        except:
            return
        old_index = old_number - 1
        if self.target.performer_count <= old_index:
            message = 'there is no performer number {}.'.format(old_number)
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        performer = self.target.performers[old_index]
        new_number = self.handle_raw_input('new number')
        try:
            new_number = int(new_number)
        except:
            return
        new_index = new_number - 1
        if self.target.performer_count <= new_index:
            message = 'there is no performer number {}.'.format(old_number)
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        self.target.performers.remove(performer)
        self.target.performers.insert(new_index, performer)

    def select_performer_name_interactively(self):
        from abjad.tools import scoretools
        self.session.menu_pieces.append('add performer')
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.items_to_number = scoretools.list_performer_names()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.session.menu_pieces.pop()
                return
            if key is None:
                continue
            else:
                self.session.menu_pieces.pop()
                return value
