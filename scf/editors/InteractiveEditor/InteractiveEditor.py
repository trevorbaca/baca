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

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
    # TODO: encapsulate menu entry formatting in menu section ONLY
    @property
    def target_attribute_tokens(self):
        result, menu_keys, display_attribute = [], [], None
        for target_attribute_tuple in self.target_attribute_tuples:
            target_attribute_name, predicate, is_read_write, default, menu_key = target_attribute_tuple[:5]
            assert menu_key not in menu_keys
            menu_keys.append(menu_key)
            spaced_attribute_name = target_attribute_name.replace('_', ' ')
            attribute_value = getattr(self.target, target_attribute_name) 
            display_value = repr(attribute_value)
            if len(target_attribute_tuple) == 6:
                display_attribute = target_attribute_tuple[5]
                if display_attribute is not None:
                    display_value = getattr(attribute_value, display_attribute)
            #if display_value is None:
            #    menu_value = '{} ({}): '.format(spaced_attribute_name, menu_key)
            #else:
            #    menu_value = '{} ({}): {}'.format(spaced_attribute_name, menu_key, display_value)
            # TODO: do we need a new, three-part token here? probably so ...
            #token = (menu_key, menu_value)
            token = (menu_key, attribute_name, attribute_value)
            result.append(token)
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

    def handle_main_menu_result(self, key):
        pass

    def run(self, user_input=None, clear=True, cache=False):
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
            self.push_breadcrumb()
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
