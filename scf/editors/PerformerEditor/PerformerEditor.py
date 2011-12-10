from baca.scf.editors.InteractiveEditor import InteractiveEditor


class PerformerEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def InstrumentEditor(self):
        import baca
        return baca.scf.editors.InstrumentEditor

    @property
    def breadcrumb(self):
        if self.target is not None and self.target.name is not None:
            return self.target.name
        else:
            return 'performer'

    @property
    def summary_lines(self):
        if not self.target.instruments:
            result = '{} (instruments not assigned)'.format(self.target.name)
        elif len(self.target.instruments) == 1 and self.target.name == \
            self.target.instruments[0].instrument_name:
            result = '{}'.format(self.target.name)
        else:
            instruments = ', '.join([x.instrument_name for x in self.target.instruments])
            result = '{} ({})'.format(self.target.name, instruments)
        result = [result]
        return result

    @property
    def target_class(self):
        from abjad.tools import scoretools
        return scoretools.Performer

    ### PUBLIC METHODS ###

    def add_instrument_interactively(self):
        editor = self.InstrumentEditor(session=self.session)
        instrument = editor.select_instrument_from_instrumenttools_interactively()
        if instrument is not None:
            self.target.instruments.append(instrument)

    def delete_instrument_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('instrument number', 1, self.target.instrument_count)
        instrument_number = getter.run()
        if self.session.backtrack():
            return
        instrument_index = instrument_number - 1
        del(self.target.instruments[instrument_index])
    
    def edit_name_interactively(self):
        if self.target.name is None:
            spaced_variable_name = 'performer name'
        else:
            spaced_variable_name = 'new performer name'
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_string(spaced_variable_name)
        name = getter.run()
        if self.session.backtrack():
            return
        self.target.name = name

    def handle_main_menu_response(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        if key == 'add':
            self.add_instrument_interactively()
        elif key == 'del':
            self.delete_instrument_interactively()
        elif key == 'mv':
            self.move_instrument_interactively()
        elif key in ('name', 'ren'):
            self.edit_name_interactively()
        elif key == 'rpn':
            return self.remove_name()
        else:
            self.edit_instrument_interactively(key)

    def edit_instrument_interactively(self, instrument_number):
        try:
            instrument_number = int(instrument_number)
        except:
            return
        if self.target.instrument_count < instrument_number:
            message = 'there is no instrument number {}'.format(instrument_number)
            self.display_cap_lines([message, ''])
            self.proceed()
            return
        instrument_index = instrument_number - 1
        instrument = self.target.instruments[instrument_index]
        instrument_editor = self.InstrumentEditor(session=self.session, target=instrument)
        instrument_editor.run()

    def make_main_menu(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu_section.menu_section_title = 'instruments'
        menu.menu_sections.append(menu_section)
        instrument_names = [x.instrument_name for x in self.target.instruments]
        menu_section.items_to_number = instrument_names
        menu_section.sentence_length_items.append(('add', 'add instrument'))
        if 0 < self.target.instrument_count:
            menu_section.sentence_length_items.append(('del', 'delete instrument'))
        if 1 < self.target.instrument_count:
            menu_section.sentence_length_items.append(('mv', 'move instrument'))
        if self.target.name is None:
            menu_section.sentence_length_items.append(('name', 'name performer'))
        else:
            menu_section.sentence_length_items.append(('ren', 'rename performer'))
            menu_section.sentence_length_items.append(('rpn', 'remove performer name'))
        return menu

    def move_instrument_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.should_clear_terminal = False
        getter.append_integer_in_closed_range('old instrument number', 1, self.target.instrument_count)
        getter.append_integer_in_closed_range('new instrument number', 1, self.target.instrument_count)
        result = getter.run()
        if self.session.backtrack():
            return
        old_instrument_number, new_instrument_number = result
        old_instrument_index, new_instrument_index = old_instrument_number - 1, new_instrument_number - 1
        instrument = self.target.instruments[old_instrument_index]
        self.target.instruments.remove(instrument)
        self.target.instruments.insert(new_instrument_index, instrument)

    def remove_name(self):
        self.target.name = None

    def set_initial_configuration_menu(self):
        from abjad.tools import instrumenttools
        menu = self.make_new_menu(where=self.where()) 
        likely_instruments = self.target.likely_instruments_based_on_performer_name
        likely_instrument_names = [x().instrument_name for x in likely_instruments]
        most_likely_instrument = self.target.most_likely_instrument_based_on_performer_name
        if most_likely_instrument is not None:
            most_likely_instrument_name = most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(most_likely_instrument_name)
            most_likely_number = most_likely_index + 1
            menu.prompt_default = str(most_likely_number)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        menu_section.menu_section_title = 'select instrument'
        if likely_instruments:
            menu_section.items_to_number = likely_instrument_names
            menu_section.sentence_length_items.append(('other', 'other instruments'))
        else:
            menu_section.items_to_number = instrumenttools.list_instrument_names()
        menu_section.sentence_length_items.append(('none', 'no instruments'))
        return menu

    def set_initial_configuration_interactively(self):
        from abjad.tools import mathtools
        self.conditionally_initialize_target()
        self.session.breadcrumbs.append(self.target.name)
        menu = self.set_initial_configuration_menu()
        while True:
            key, value = menu.run()
            if self.session.backtrack():
                self.session.breadcrumbs.pop()
                return
            elif key is None:
                continue
            elif mathtools.is_integer_equivalent_expr(key):
                instrument_name = value
                instrument_name = instrument_name.title()
                instrument_name = instrument_name.replace(' ', '')
                exec('from abjad import *')
                exec('instrument = instrumenttools.{}()'.format(instrument_name))
                self.target.instruments.append(instrument)
                break
            elif key == 'none':
                break
            elif key == 'other':
                editor = self.InstrumentEditor(session=self.session)
                instrument = editor.select_instrument_from_instrumenttools_interactively()
                if instrument is not None:
                    self.target.instruments.append(instrument)
                break
            else:
                break
        self.session.breadcrumbs.pop()
