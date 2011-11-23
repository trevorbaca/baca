from baca.scf.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        assert isinstance(target, (type(self.target_class()), type(None)))
        self.target = target

    ### PUBLIC METHODS ###

    def conditionally_set_target_attr(self, attr_name, attr_value):
        if not self.session.session_is_complete:
            setattr(self.target, attr_name, attr_value)

    def edit_interactively(self):
        self.session.menu_pieces.append(self.menu_piece)
        self.target = self.target or self.target_class()
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.handle_main_menu_response(key, value):
                break
            if self.session.session_is_complete:
                break
        self.session.menu_pieces.pop()
        target = self.target
        self.target = None
        return target
