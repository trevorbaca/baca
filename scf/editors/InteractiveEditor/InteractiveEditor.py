from baca.scf.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        if target is not None:
            assert isinstance(target, type(self.target_class()))
        self.target = target

    ### OVERLOADS ###

    def __repr__(self):
        if self.target is None:
            summary = ''
        else:
            summary = 'target={!r}'.format(self.target)
        return '{}({})'.format(type(self).__name__, summary)

    ### PUBLIC ATTRIBUTES ###
    
    # TODO: rename to target_attribute_keyed_menu_tuples
    @property
    def target_attribute_menu_entries(self):
        result = []
        target_attribute_names, menu_keys, left_hand_labels = [], [], []
        for target_attribute_name, predicate, is_read_write, default in self.target_attribute_tuples:
            target_attribute_names.append(target_attribute_name)
            menu_key = self.attribute_name_to_menu_key(target_attribute_name, menu_keys)
            assert menu_key not in menu_keys
            menu_keys.append(menu_key)
            spaced_attribute_name = target_attribute_name.replace('_', ' ')
            left_hand_label = '{} ({}):'.format(spaced_attribute_name, menu_key)
            left_hand_labels.append(left_hand_label)
        left_hand_label_width = max([len(x) for x in left_hand_labels])
        for left_hand_label, target_attribute_name, menu_key in zip(
            left_hand_labels, target_attribute_names, menu_keys):
            menu_value = '{:<{width}} {!r}'.format(
                left_hand_label, getattr(self.target, target_attribute_name), width=left_hand_label_width) 
            display_key = False
            keyed_menu_tuple = (menu_key, menu_value, display_key)
            result.append(keyed_menu_tuple)
        return result

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

    def conditionally_initialize_target(self):
        self.target = self.target or self.target_class()

    def conditionally_set_target_attribute(self, attribute_name, attribute_value):
        if not self.session.is_complete:
            setattr(self.target, attribute_name, attribute_value)

    def handle_main_menu_response(self, key, value):
        pass

    def run(self, user_input=None):
        if user_input is not None:
            self.session.user_input = user_input
        self.breadcrumbs.append(self.breadcrumb)
        self.session.backtrack_preservation_is_active = True
        self.conditionally_initialize_target()
        self.session.backtrack_preservation_is_active = False
        self.breadcrumbs.pop()
        if self.backtrack():
            return
        while True:
            self.breadcrumbs.append(self.breadcrumb)
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.backtrack():
                break
            elif key is None:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_response(key, value)
            if self.backtrack():
                break
            self.breadcrumbs.pop()
        self.breadcrumbs.pop()
