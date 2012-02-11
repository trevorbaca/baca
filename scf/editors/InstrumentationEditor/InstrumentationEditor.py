from abjad.tools import scoretools
from abjad.tools import sequencetools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.PerformerEditor import PerformerEditor


class InstrumentationEditor(InteractiveEditor):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'performers'

    @property
    def summary_lines(self):
        result = []
        for performer in self.target.performers:
            performer_editor = PerformerEditor(session=self.session, target=performer)
            result.extend(performer_editor.summary_lines)
        return result

    target_class = scoretools.InstrumentationSpecifier

    target_item_class = scoretools.Performer

    @property
    def target_items(self):
        return self.target.performers

    ### PUBLIC METHODS ###

    # performer creation and config can probably be combined in performer editor
    def add_performers_interactively(self):
        from abjad.tools import scoretools
        try_again = False
        while True:
            if self.backtrack():
                return
            self.push_backtrack()
            performer_names = self.select_performer_names_interactively()
            self.pop_backtrack()
            if self.backtrack():
                return
            elif performer_names:
                performers = []
                for performer_name in performer_names:
                    performer = scoretools.Performer(performer_name)
                    performer_editor = PerformerEditor(session=self.session, target=performer)
                    self.push_breadcrumb('add performers')
                    self.push_backtrack()
                    performer_editor.set_initial_configuration_interactively()
                    self.pop_backtrack()
                    self.pop_breadcrumb()
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

    # TODO: abstract up to ListEditor.delete_items_interactively
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
        performer_editor = PerformerEditor(session=self.session, target=performer)
        performer_editor.run()

    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.target.performers[performer_index]
        except:
            performer = None
        return performer

    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'add':
            self.add_performers_interactively()
        elif result == 'del':
            self.delete_performers_interactively()
        elif result == 'mv':
            self.move_performer_interactively()
        else:
            self.edit_performer_interactively(result)

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.summary_lines
        section.return_value_attribute = 'number'
        section = menu.make_new_section(is_keyed=False)
        section.append(('add', 'add performers'))
        if 0 < self.target.performer_count:
            section.append(('del', 'delete performers'))
        if 1 < self.target.performer_count:
            section.append(('mv', 'move performers'))
        return menu

    def move_performer_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_in_range('old number', 1, self.target.performer_count)
        getter.append_integer_in_range('new number', 1, self.target.performer_count)
        result = getter.run()
        if self.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        performer = self.target.performers[old_index]
        self.target.performers.remove(performer)
        self.target.performers.insert(new_index, performer)

    def select_performer_names_interactively(self, clear=True, cache=False):
        from abjad.tools import scoretools
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True, is_ranged=True)
        performer_names, performer_abbreviations = [], []
        performer_pairs = scoretools.list_primary_performer_names()
        performer_pairs = [(x[1].split()[-1].strip('.'), x[0]) for x in performer_pairs]
        performer_pairs.append(('perc', 'percussionist'))
        performer_pairs.sort(lambda x, y: cmp(x[1], y[1]))
        section.tokens = performer_pairs
        section.return_value_attribute = 'body'
        while True:
            self.push_breadcrumb('add performers')
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return result
