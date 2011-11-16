from baca.scf.menuing.InteractiveEditor import InteractiveEditor


class InstrumentationEditor(InteractiveEditor):

    def __init__(self, session=None, instrumentation=None):
        self.session = session
        self.instrumentation = instrumentation

    ### PUBLIC METHODS ###

    def edit(self):
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        self.session.menu_pieces.append('edit instrumentation')
        self.instrumentation = self.instrumentation or scoretools.Instrumentation()
        while True:
            menu = self.Menu(where=self.where(), session=self.session)
            menu_section = self.MenuSection()
            menu_section.menu_section_title = 'performers'
            menu_section.items_to_number = self.instrumentation_to_lines(self.instrumentation)
            menu_section.sentence_length_items.append(('add', 'add performer'))
            menu.menu_sections.append(menu_section)
            key, value = menu.run() # make it so no need to pass in session
            if key is None:
                pass
            elif key == 'b':
                break
            elif key == 'add':
                self.add_performer_to_instrumentation_interactively()
            elif mathtools.is_integer_equivalent_expr(key):
                pass
            if session.test_is_complete or session.user_input_is_consumed:
                break 
        session.menu_pieces.pop()

    def instrumentation_to_lines(self, instrumentation):
        result = []
        for performer in instrumentation.performers:
            if not performer.instruments:
                result.append('{}: (none)'.format(performer.designation))
            else:
                instruments = ', '.join([x.instrument_name.contents_string for x in performer.instruments])
                result.append('{}: {}'.format(performer.designation, instruments))
        return result
