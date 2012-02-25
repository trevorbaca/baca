from abjad.tools import sequencetools
from baca.scf.editors.InteractiveEditor import InteractiveEditor


class ListEditor(InteractiveEditor):

    ### READ-ONLY ATTRIBUTES ###

    target_item_class = None
    target_item_editor_class = None
    target_item_identifier = 'element'
    target_items_identifier = 'elements'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return list

    @property
    def summary_lines(self):
        result = []
        for target_item in self.target_items:
            result.append(repr(target_item))
        return result

    @property
    def target_items(self):
        return self.target

    ### PUBLIC METHODS ###

    def add_target_item_interactively(self):
        if self.target_item_getter_configuration_method:
            getter = self.make_getter(where=self.where())
            self.target_item_getter_configuration_method(getter, self.target_item_identifier)
            self.push_backtrack()
            target_item_initialization_token = getter.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            target_item = self.target_item_class(target_item_initialization_token)
        else:
            target_item = self.target_item_class()
        self.target_items.append(target_item)

    def edit_target_item_interactively(self, target_item_number):
        target_item = self.get_target_itme_from_target_item_number(target_item_number)
        if target_item is not None:
            target_item_editor = self.target_item_editor_class(session=self.session, target=target_item)
            target_item_editor.run()

    def get_target_item_from_target_item_number(self, target_item_number):
        try:
            return self.target_items[int(target_item_number) - 1]
        except:
            pass

    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'add':
            self.add_target_item_interactively()
        elif result == 'rm':
            self.remove_target_items_interactively()
        elif result == 'mv':
            self.move_target_item_interactively()
        else:
            self.edit_target_item_interactively(result)

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.summary_lines
        section.return_value_attribute = 'number'
        section = menu.make_section()
        section.append(('add', 'add {}'.format(self.target_item_identifier)))
        if 0 < len(self.target_items):
            section.append(('rm', 'delete {}'.format(self.target_items_identifier)))
        if 1 < len(self.target_items):
            section.append(('mv', 'move {}'.format(self.target_items_identifier)))
        return menu

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
