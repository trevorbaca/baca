from abjad.tools import mathtools
from abjad.tools import sequencetools
from scf.editors.InteractiveEditor import InteractiveEditor


class ListEditor(InteractiveEditor):

    ### READ-ONLY ATTRIBUTES ###

    target_item_class = None
    target_item_creator_class = None
    target_item_creator_class_kwargs = {}
    target_item_editor_class = None
    target_item_getter_configuration_method = None
    target_item_identifier = 'element'
    target_manifest = None

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or self.target_class_human_readable_name

    @property
    def target_items(self):
        return self.target

    @property
    def target_items_identifier(self):
        if hasattr(self, '_target_items_identifier'):
            return self._target_items_identifer
        else:
            return self.pluralize_string(self.target_item_identifier)

    @property
    def target_summary_lines(self):
        result = []
        for target_item in self.target_items:
            result.append(self.get_one_line_menuing_summary(target_item))
        return result

    ### PUBLIC METHODS ###

    # TODO: change name to self.add_target_items_interactively()
    def add_target_item_interactively(self):
        if self.target_item_creator_class:
            target_item_creator = self.target_item_creator_class(
                session=self.session, **self.target_item_creator_class_kwargs)
            self.push_backtrack()
            result = target_item_creator.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            result = result or target_item_creator.target
        elif self.target_item_getter_configuration_method:
            getter = self.make_getter(where=self.where())
            self.target_item_getter_configuration_method(getter, self.target_item_identifier)
            self.push_backtrack()
            target_item_initialization_token = getter.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            #target_item = self.target_item_class(target_item_initialization_token)
            result = self.target_item_class(target_item_initialization_token)
        else:
            #target_item = self.target_item_class()
            result = self.target_item_class()
        if result is None:
            result = []
        if isinstance(result, list):
            target_items = result
        else:
            target_items = [result]
        #if target_item:
        #    self.target_items.append(target_item)
        self.target_items.extend(target_items)

    def edit_target_item_interactively(self, target_item_number):
        target_item = self.get_target_item_from_target_item_number(target_item_number)
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
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_target_item_interactively(result)
        else:
            InteractiveEditor.handle_main_menu_result(self, result)

    def make_main_menu(self):
        menu, attribute_management_section = self.make_menu(where=self.where(), 
            is_keyed=getattr(self.target_manifest, 'is_keyed', False))
        attribute_management_section.tokens = self.target_attribute_tokens
        attribute_management_section.show_existing_values = True
        item_management_section = menu.make_section(is_parenthetically_numbered=True)
        item_management_section.tokens = self.target_summary_lines
        item_management_section.return_value_attribute = 'number'
        command_section = menu.make_section()
        command_section.append(('add', 'add elements'))
        if 0 < len(self.target_items):
            command_section.append(('rm', 'remove elements'))
        if 1 < len(self.target_items):
            command_section.append(('mv', 'move elements'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('done', 'done'))
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
        getter.append_argument_range(self.target_items_identifier, self.target_summary_lines)
        argument_range = getter.run()
        if self.backtrack():
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        target_items = self.target_items[:]
        target_items = sequencetools.remove_sequence_elements_at_indices(target_items, indices)
        self.target_items[:] = target_items
