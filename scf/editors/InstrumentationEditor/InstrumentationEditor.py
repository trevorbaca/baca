from baca.scf.editors.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def breadcrumb(self):
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

    # performer creation and config can probably be combined in performer editor
    def add_performer_interactively(self):
        from abjad.tools import scoretools
        while True:
            if self.session.backtrack():
                return
            self.session.backtrack_preservation_is_active = True
            performer_name = self.select_performer_name_interactively()
            self.session.backtrack_preservation_is_active = False
            if self.session.backtrack():
                return
            elif performer_name:
                performer = scoretools.Performer(performer_name)
                performer_editor = self.PerformerEditor(session=self.session, target=performer)
                self.breadcrumbs.append('add performer')
                self.session.backtrack_preservation_is_active = True
                performer_editor.set_initial_configuration_interactively()
                self.session.backtrack_preservation_is_active = False
                self.breadcrumbs.pop()
                if self.session.backtrack():
                    continue
                self.target.performers.append(performer)
                break

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
        section = self.MenuSection()
        if self.target.performer_count:
            section.section_title = 'performers'
        menu.sections.append(section)
        section.items_to_number = self.summary_lines
        section.sentence_length_items.append(('add', 'add performer'))
        if 0 < self.target.performer_count:
            section.sentence_length_items.append(('del', 'delete performer'))
        if 1 < self.target.performer_count:
            section.sentence_length_items.append(('mv', 'move performer'))
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
        self.breadcrumbs.append('add performer')
        menu = self.make_new_menu(where=self.where())
        section = self.MenuSection()
        menu.sections.append(section)
        section.items_to_number = scoretools.list_performer_names()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.breadcrumbs.pop()
                return
            if key is None:
                continue
            else:
                self.breadcrumbs.pop()
                return value
