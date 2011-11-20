from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentEditor(InteractiveEditor):

    def __init__(self, session=None, instrument=None):
        InteractiveEditor.__init__(self, session=session)
        self.instrument = instrument

    ### PUBLIC METHODS ###

    def edit_interactively(self):
        self.session.menu_pieces.append(self.instrument.instrument_name)
        while True:
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.handle_main_menu_response(key, value):
                break
        self.session.menu_pieces.pop()

    def handle_main_menu_response(self, key, value):
        '''Return true when calling function should break.
        '''
        if key == 'b':
            return True
        elif key == 'in':
            self.edit_instrument_name_interactively()
        elif key == 'inm':
            self.edit_instrument_name_markup_interactively()
        elif key == 'sin':
            self.edit_short_instrument_name_interactively()
        elif key == 'sinm':
            self.edit_short_instrument_name_markup_interactively()

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.sentence_length_items.append(('in', 'instrument name'))
        menu_section.sentence_length_items.append(('inm', 'instrument name markup'))
        menu_section.sentence_length_items.append(('sin', 'short instrument name'))
        menu_section.sentence_length_items.append(('sinm', 'short instrument name markup'))
        return menu
