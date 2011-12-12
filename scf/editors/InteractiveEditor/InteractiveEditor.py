from baca.scf.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        if target is not None:
            assert isinstance(target, type(self.target_class()))
        self.target = target

    ### PUBLIC METHODS ###

    def attribute_name_to_menu_key(self, attribute_name, menu_keys):
        found_menu_key = False        
        attr_parts = attribute_name.split('_')
        i = 1
        while True:
            menu_key = ''.join([part[:i] for part in attr_parts])
            if menu_key not in menu_keys:
                break
            i = i + 1
        return menu_key

    def conditionally_initialize_target(self):
        self.target = self.target or self.target_class()

    def conditionally_set_target_attr(self, attr_name, attr_value):
        if not self.session.is_complete:
            setattr(self.target, attr_name, attr_value)

    def range_string_to_numbers(self, range_string, range_start=None, range_stop=None):
        numbers = []
        range_parts = range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(range_start, range_stop + 1))    
            elif '-' in range_part:
                start, stop = range_part.split('-') 
                start, stop = int(start), int(stop)
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = int(range_part)
                numbers.append(number)
        return numbers

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
