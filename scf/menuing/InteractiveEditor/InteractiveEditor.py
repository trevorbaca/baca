from baca.scf.SCFObject import SCFObject


class InteractiveEditor(SCFObject):
    
    def __init__(self, session=None):
        SCFObject.__init__(self, session=session)

    ### PUBLIC METHODS ###

    def edit_interactively(self):
        self.session.menu_pieces.append(self.menu_piece)
        self.target = self.target or self.target_class()
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.handle_main_menu_response(key, value):
                break
        self.session.menu_pieces.pop()
        target = self.target
        self.target = None
        return target
