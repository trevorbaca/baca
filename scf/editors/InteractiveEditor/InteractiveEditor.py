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
    
    @property
    def target_attribute_menu_entries(self):
        result = []
        menu_keys = []
        for target_attribute_name, predicate, is_read_write in self.target_attribute_tuples:
            menu_key = self.attribute_name_to_menu_key(target_attribute_name, menu_keys)
            assert menu_key not in menu_keys
            menu_keys.append(menu_key)
            value = target_attribute_name.replace('_', ' ')
            value = '{} ({!r})'.format(value, getattr(self.target, target_attribute_name))
            pair = (menu_key, value)
            result.append(pair)
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
        if self.session.backtrack():
            return
        while True:
            self.breadcrumbs.append(self.breadcrumb)
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.session.backtrack():
                break
            elif key is None:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_response(key, value)
            if self.session.backtrack():
                break
            self.breadcrumbs.pop()
        self.breadcrumbs.pop()
