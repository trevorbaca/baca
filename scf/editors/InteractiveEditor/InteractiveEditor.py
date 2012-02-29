from scf.core.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        if target is not None:
            assert isinstance(target, self.target_class)
        self.target = target
        self.initialize_attributes_in_memory()

    ### OVERLOADS ###

    def __repr__(self):
        if self.target is None:
            summary = ''
        else:
            summary = 'target={!r}'.format(self.target)
        return '{}({})'.format(self.class_name, summary)

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
    @property
    def attributes_in_memory(self):
        return self._attributes_in_memory

    @property
    def breadcrumb(self):
        return self.target_name or self.target_class_human_readable_name

    @property
    def has_target(self):
        return self.target is not None

    @property
    def target_attribute_tokens(self):
        if hasattr(self, 'target_manifest'):
            return self.make_target_attribute_tokens_from_target_manifest()
        elif hasattr(self, 'target_attribute_tuples'):
            return self.make_target_attribute_tokens_from_target_attribute_tuples()
        else:
            raise ValueError

    @property
    def target_class_human_readable_name(self):
        return self.change_string_to_human_readable_string(self.target_class.__name__)

    @property
    def target_name(self):
        pass

    ### PUBLIC METHODS ###

    def attribute_name_to_menu_key(self, attribute_name, menu_keys):
        found_menu_key = False        
        attribute_parts = attribute_name.split('_')
        i = 1
        while True:
            menu_key = ''.join([part[:i] for part in attribute_parts])
            if menu_key not in menu_keys:
                break
            i = i + 1
        return menu_key

    def clean_up_attributes_in_memory(self):
        if self.attributes_in_memory:
            if self.target is None:
                self.initialize_target_from_attributes_in_memory()
            else:
                raise ValueError('Target and in-memory attributes can not both exist.')

    def conditionally_initialize_target(self):
        self.target = self.target or self.target_class()

    def conditionally_set_target_attribute(self, attribute_name, attribute_value):
        if self.target:
            if not self.session.is_complete:
                setattr(self.target, attribute_name, attribute_value)
        else:
            self.attributes_in_memory[attribute_name] = attribute_value

    def handle_main_menu_result(self, result):
        attribute_name = self.target_manifest.menu_key_to_attribute_name(result)
        existing_value = self.menu_key_to_existing_value(result)
        kwargs = self.menu_key_to_delegated_editor_kwargs(result)
        editor = self.target_manifest.menu_key_to_editor(
            result, session=self.session, existing_value=existing_value, **kwargs)
        if editor is not None:
            result = editor.run()
            if self.backtrack():
                return
            if hasattr(editor, 'target'):
                attribute_value = editor.target
            else:
                attribute_value = result
            self.conditionally_set_target_attribute(attribute_name, attribute_value)

    def initialize_attributes_in_memory(self):
        self._attributes_in_memory = {}

    def initialize_target_from_attributes_in_memory(self):
        target = self.target_class(**self.attributes_in_memory)
        self.target = target
        self.initialize_attributes_in_memory()

    def make_main_menu(self):
        is_keyed = self.target_manifest.is_keyed
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_keyed=is_keyed)
        section.tokens = self.target_attribute_tokens
        section.show_existing_values = True
        return menu

    def make_target_attribute_tokens_from_target_attribute_tuples(self):
        result, menu_keys, display_attribute = [], [], None
        for target_attribute_tuple in self.target_attribute_tuples:
            target_attribute_name, predicate, is_read_write, default, menu_key = target_attribute_tuple[:5]
            assert menu_key not in menu_keys
            menu_keys.append(menu_key)
            menu_body = target_attribute_name.replace('_', ' ')
            attribute_value = getattr(self.target, target_attribute_name) 
            if hasattr(attribute_value, '__len__') and not len(attribute_value):
                attribute_value = None
            existing_value = self.get_one_line_menuing_summary(attribute_value)
            if 6 <= len(target_attribute_tuple):
                display_attribute = target_attribute_tuple[5]
                if display_attribute is not None:
                    existing_value = getattr(attribute_value, display_attribute)
            token = (menu_key, menu_body, existing_value)
            result.append(token)
        return result

    def make_target_attribute_tokens_from_target_manifest(self):
        result = []
        for attribute_detail in self.target_manifest.attribute_details:
            if attribute_detail.is_null:
                result.append(())
                continue
            menu_key = attribute_detail.menu_key
            target_attribute_name = attribute_detail.name
            menu_body = attribute_detail.human_readable_name
            if self.target:
                attribute_value = getattr(self.target, target_attribute_name)
            else:
                attribute_value = self.attributes_in_memory.get(target_attribute_name)
            if hasattr(attribute_value, '__len__') and not len(attribute_value):
                attribute_value = None
            existing_value = self.get_one_line_menuing_summary(attribute_value)
            token = (menu_key, menu_body, existing_value)
            result.append(token)
        return result

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        return {}
        
    def menu_key_to_existing_value(self, menu_key):
        attribute_name = self.target_manifest.menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

    def run(self, breadcrumb=None, cache=False, clear=True, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        self.push_backtrack()
        self.conditionally_initialize_target()
        self.pop_backtrack()
        self.pop_breadcrumb()
        if self.backtrack():
            self.restore_breadcrumbs(cache=cache)
            return
        while True:
            self.push_breadcrumb(breadcrumb=breadcrumb)
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.clean_up_attributes_in_memory()
