from abjad.tools import pitchtools
from abjad.tools import sequencetools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.ListEditor import ListEditor
from baca.scf.editors.PitchRangeEditor import PitchRangeEditor
from baca.scf.menuing.UserInputGetter import UserInputGetter


class PitchRangeInventoryEditor(InteractiveEditor):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'pitch-range inventory'

    @property
    def summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result

    target_class = pitchtools.PitchRangeInventory

    target_item_getter_configuration_method = UserInputGetter.append_symbolic_pitch_range_string

    target_item_class = pitchtools.PitchRange

    target_item_editor_class = PitchRangeEditor

    target_item_identifier = 'pitch range'

    @property
    def target_items(self):
        return self.target

    target_items_identifier = 'pitch ranges'

    ### PUBLIC METHODS ####

    # TODO: abstract up to ListEditor.add_item_interactively()
    def add_target_item_interactively(self):
        getter = self.make_getter(where=self.where())
        self.target_item_getter_configuration_method(getter, self.target_item_identifier)
        self.push_backtrack()
        target_item_initialization_token = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        target_item = self.target_item_class(target_item_initialization_token)
        self.target_items.append(target_item)

    # TODO: abstract up to ListEditor.delete_items_interactively()
    def remove_target_items_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_argument_range(self.target_items_identifier, self.summary_lines)
        argument_range = getter.run()
        if self.backtrack():
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        target_items = self.target_items[:]
        target_items = sequencetools.remove_sequence_elements_at_indices(target_items, indices)
        self.target_items[:] = target_items

    # TODO: abstract up to ListEditor.edit_item_interactively()
    def edit_target_item_interactively(self, target_item_number):
        target_item = self.get_target_itme_from_target_item_number(target_item_number)
        if target_item is not None:
            target_item_editor = self.target_item_editor_class(session=self.session, target=target_item)
            target_item_editor.run()

    # TODO: abstract up to ListEditor.edit_item_interactively()
    def get_target_item_from_target_item_number(self, target_item_number):
        try:
            return self.target_items[int(target_item_number) - 1]
        except:
            pass

    # TODO: abstract up to ListEditor.edit_item_interactively()
    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'add':
            self.add_target_item_interactively()
        elif result == 'del':
            self.remove_target_items_interactively()
        elif result == 'mv':
            self.move_target_item_interactively()
        else:
            self.edit_target_item_interactively(result)

    # TODO: abstract up to ListEditor.edit_item_interactively()
    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.summary_lines
        section.return_value_attribute = 'number'
        section = menu.make_section(is_keyed=False)
        section.append(('add', 'add {}'.format(self.target_item_identifier)))
        if 0 < len(self.target_items):
            section.append(('del', 'delete {}'.format(self.target_items_identifier)))
        if 1 < len(self.target_items):
            section.append(('mv', 'move {}'.format(self.target_items_identifier)))
        return menu

    # TODO: abstract up to ListEditor.edit_item_interactively()
    def move_target_item_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_integer_in_range('old number', 1, len(self.target_items))
        getter.append_integer_in_range('new number', 1, len(self.target_items))
        result = getter.run()
        if self.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        target_item = self.target_items[old_index]
        self.target_items.remove(target_item)
        self.target_items.insert(new_index, target_item)
