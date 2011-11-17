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
        self.instrumentation = self.instrumentation or scoretools.InstrumentationSpecifier()
        while True:
            menu = self.Menu(where=self.where(), session=self.session)
            menu_section = self.MenuSection()
            menu_section.menu_section_title = 'performers'
            menu_section.items_to_number = self.instrumentation_to_lines(self.instrumentation)
            menu_section.sentence_length_items.append(('add', 'add performer'))
            menu.menu_sections.append(menu_section)
            key, value = menu.run()
            if key is None:
                pass
            elif key == 'b':
                break
            elif key == 'add':
                self.add_performer_to_instrumentation_interactively()
            else:
                try:
                    if mathtools.is_integer_equivalent_number(int(key)):
                        pass
                except ValueError:
                    pass
            if self.session.session_is_complete:
                break 
        self.session.menu_pieces.pop()

    def instrumentation_to_lines(self, instrumentation):
        result = []
        for performer in instrumentation.performers:
            if not performer.instruments:
                result.append('{}: (none)'.format(performer.designation))
            else:
                instruments = ', '.join([x.instrument_name.contents_string for x in performer.instruments])
                result.append('{}: {}'.format(performer.designation, instruments))
        return result
