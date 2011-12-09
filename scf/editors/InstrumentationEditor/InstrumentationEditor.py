from baca.scf.editors.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def menu_title_contribution(self):
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

    def add_performer_interactively(self):
        from abjad.tools import scoretools
        # creation and initial config can probably be combined in the performer editor
        performer_name = self.select_performer_name_interactively()
        if self.session.backtrack():
            return
        elif performer_name:
            performer = scoretools.Performer(performer_name)
            self.target.performers.append(performer)
            performer_editor = self.PerformerEditor(session=self.session, target=performer)
            performer_editor.set_initial_configuration_interactively()
            # dunno if backtrack check needs to happen here or not, probably not

    def delete_performer_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('performer number', 1, self.target.performer_count)
        performer_number = getter.run()
        if self.session.backtrack():
            return
        performer_index = performer_number - 1
        del(self.target.performers[performer_index])

    def edit_performer_interactively(self, performer_number):
        try:
            performer_number = int(performer_number)
        except:
            return
        performer = self.get_performer_from_performer_number(performer_number)
        performer_editor = self.PerformerEditor(session=self.session, target=performer)
        performer_editor.run()

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
        if self.target.performer_count:
            menu_section.menu_section_title = 'performers'
        menu.menu_sections.append(menu_section)
        menu_section.items_to_number = self.summary_lines
        menu_section.sentence_length_items.append(('add', 'add performer'))
        if 0 < self.target.performer_count:
            menu_section.sentence_length_items.append(('del', 'delete performer'))
        if 1 < self.target.performer_count:
            menu_section.sentence_length_items.append(('mv', 'move performer'))
        return menu

    def move_performer_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('old number', 1, self.target.performer_count)
        getter.append_integer_in_closed_range('new number', 1, self.target.performer_count)
        result = getter.run()
        if self.session.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        performer = self.target.performers[old_index]
        self.target.performers.remove(performer)
        self.target.performers.insert(new_index, performer)

    def select_performer_name_interactively(self):
        from abjad.tools import scoretools
        self.session.menu_title_contributions.append('add performer')
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.items_to_number = scoretools.list_performer_names()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.session.menu_title_contributions.pop()
                return
            if key is None:
                continue
            else:
                self.session.menu_title_contributions.pop()
                return value
