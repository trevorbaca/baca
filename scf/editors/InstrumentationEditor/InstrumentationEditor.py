from abjad.tools import sequencetools
from baca.scf.editors.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def PerformerEditor(self):
        import baca
        return baca.scf.editors.PerformerEditor

    @property
    def breadcrumb(self):
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

    # performer creation and config can probably be combined in performer editor
    def add_performers_interactively(self):
        from abjad.tools import scoretools
        try_again = False
        while True:
            if self.backtrack():
                return
            self.session.backtrack_preservation_is_active = True
            performer_names = self.select_performer_names_interactively()
            self.session.backtrack_preservation_is_active = False
            if self.backtrack():
                return
            elif performer_names:
                performers = []
                for performer_name in performer_names:
                    performer = scoretools.Performer(performer_name)
                    performer_editor = self.PerformerEditor(session=self.session, target=performer)
                    self.breadcrumbs.append('add performers')
                    self.session.backtrack_preservation_is_active = True
                    performer_editor.set_initial_configuration_interactively()
                    self.session.backtrack_preservation_is_active = False
                    self.breadcrumbs.pop()
                    if self.backtrack():
                        performers = []
                        try_again = True
                        break
                    performers.append(performer)
                for performer in performers:
                    self.target.performers.append(performer)
                if try_again:
                    continue
                break

    def delete_performers_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_argument_range('performers', self.summary_lines)
        result = getter.run()
        if self.backtrack():
            return
        performer_indices = [performer_number - 1 for performer_number in result]
        performer_indices = list(reversed(sorted(set(performer_indices))))
        performers = self.target.performers
        performers = sequencetools.remove_sequence_elements_at_indices(performers, performer_indices)
        self.target.performers[:] = performers

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
            self.add_performers_interactively()
        elif key == 'del':
            self.delete_performers_interactively()
        elif key == 'mv':
            self.move_performer_interactively()
        else:
            self.edit_performer_interactively(key)

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        tuples = [('', x) for x in self.summary_lines]
        section.menu_entry_tuples = tuples
        section.number_menu_entries = True
        section = menu.make_new_section()
        section.menu_entry_tuples.append(('add', 'add performers'))
        if 0 < self.target.performer_count:
            section.menu_entry_tuples.append(('del', 'delete performers'))
        if 1 < self.target.performer_count:
            section.menu_entry_tuples.append(('mv', 'move performers'))
        section.display_keys = False
        return menu

    def move_performer_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_in_closed_range('old number', 1, self.target.performer_count)
        getter.append_integer_in_closed_range('new number', 1, self.target.performer_count)
        result = getter.run()
        if self.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        performer = self.target.performers[old_index]
        self.target.performers.remove(performer)
        self.target.performers.insert(new_index, performer)

    def select_performer_names_interactively(self):
        from abjad.tools import scoretools
        self.breadcrumbs.append('add performers')
        menu, section = self.make_new_menu(where=self.where())
        menu.allow_argument_range = True
        performer_names = scoretools.list_primary_performer_names()
        performer_names.append('percussionist')
        performer_names.sort()
        section.menu_entry_tuples = [('', x) for x in performer_names]
        section.number_menu_entries = True
        while True:
            key, value = menu.run()
            if self.backtrack():
                self.breadcrumbs.pop()
                return
            if key is None:
                continue
            else:
                self.breadcrumbs.pop()
                return value
