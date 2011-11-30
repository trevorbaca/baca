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

    def edit_interactively(self):
        result = False
        self.session.menu_pieces.append(self.menu_piece)
        if self.conditionally_initialize_target():
            self.session.menu_pieces.pop()
            self.session.menu_pieces.append(self.menu_piece)
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.session.is_complete:
                result = True
                break
            tmp = self.handle_main_menu_response(key, value)
            if tmp == 'back':
                break
            elif tmp == True:
                result = True
                break
            elif tmp in (False, None):
                pass
            else:
                raise ValueError(repr(tmp))
        self.session.menu_pieces.pop()
        return result
