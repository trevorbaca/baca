from baca.scf.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        assert isinstance(target, (type(self.target_class()), type(None)))
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

    def run(self, user_input=None):
        if user_input is not None:
            self.session.user_input = user_input
        self.session.menu_title_contributions.append(self.menu_title_contribution)
        if self.conditionally_initialize_target():
            # can the following line be removed?
            self.session.menu_title_contributions.append(self.menu_title_contribution)
        if self.session.backtrack():
            self.session.menu_title_contributions.pop()
            return True
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.session.backtrack():
                break
            elif key is None:
                continue
            self.handle_main_menu_response(key, value)
            if self.session.backtrack():
                break
        self.session.menu_title_contributions.pop()

    def get_positive_integer_interactively(self, spaced_variable_name):
        user_response = self.handle_raw_input(spaced_variable_name)
        message = '{} must be positive integer.'.format(spaced_variable_name)
        try:
            integer = int(user_response)
        except ValueError:
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        if integer <= 0:
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        return integer
