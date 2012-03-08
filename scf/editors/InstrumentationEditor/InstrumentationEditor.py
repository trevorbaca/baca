from abjad.tools import scoretools
from abjad.tools import sequencetools
from scf import getters
from scf import selectors
from scf import wizards
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.PerformerEditor import PerformerEditor
from scf.editors.TargetManifest import TargetManifest


# TODO: inherit from ListEditor and streamline everything
class InstrumentationEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = scoretools.Performer
    target_manifest = TargetManifest(scoretools.InstrumentationSpecifier,
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'performers'

    @property
    def target_summary_lines(self):
        result = []
        for performer in self.target.performers:
            performer_editor = PerformerEditor(session=self.session, target=performer)
            result.extend(performer_editor.target_summary_lines)
        return result

    @property
    def target_items(self):
        return self.target.performers

    ### PUBLIC METHODS ###

    def add_performers_interactively(self):
        wizard = wizards.PerformerCreationWizard(session=self.session, is_ranged=True)
        performers = wizard.run()
        if self.backtrack():
            return
        self.target.performers.extend(performers)

    # TODO: replace with list editor
    def edit_performer_interactively(self, performer_number):
        try:
            performer_number = int(performer_number)
        except:
            return
        performer = self.get_performer_from_performer_number(performer_number)
        performer_editor = PerformerEditor(session=self.session, target=performer)
        performer_editor.run()

    # TODO: replace with list editor
    def get_performer_from_performer_number(self, performer_number):
        assert isinstance(performer_number, int)
        performer_index = performer_number - 1
        try:
            performer = self.target.performers[performer_index]
        except:
            performer = None
        return performer

    # TODO: replace with list editor
    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'add':
            self.add_performers_interactively()
        elif result == 'rm':
            self.remove_performers_interactively()
        elif result == 'mv':
            self.move_performer_interactively()
        else:
            self.edit_performer_interactively(result)

    # TODO: replace with list editor
    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.target_summary_lines
        section.return_value_attribute = 'number'
        section = menu.make_section(is_keyed=False)
        section.append(('add', 'add performers'))
        if 0 < self.target.performer_count:
            section.append(('rm', 'delete performers'))
        if 1 < self.target.performer_count:
            section.append(('mv', 'move performers'))
        return menu

    # TODO: replace with list editor
    def move_performer_interactively(self):
        getter = self.make_getter(where=self.where())
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

    # TODO: replace with list editor
    def remove_performers_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_argument_range('performers', self.target_summary_lines)
        result = getter.run()
        if self.backtrack():
            return
        performer_indices = [performer_number - 1 for performer_number in result]
        performer_indices = list(reversed(sorted(set(performer_indices))))
        performers = self.target.performers
        performers = sequencetools.remove_sequence_elements_at_indices(performers, performer_indices)
        self.target.performers[:] = performers
