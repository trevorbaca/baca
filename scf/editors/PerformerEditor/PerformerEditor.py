from abjad.tools import instrumenttools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
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
    def instrument_names(self):
        return [instrument.instrument_name for instrument in self.target.instruments]

    @property
    def summary_lines(self):
        if not self.target.instruments:
            result = '{} (no instruments)'.format(self.target.name)
        elif len(self.target.instruments) == 1 and self.target.name == \
            self.target.instruments[0].instrument_name:
            result = '{}'.format(self.target.name)
        else:
            #instruments = ', '.join([x.instrument_name for x in self.target.instruments])
            instruments = ', '.join(self.instrument_names)
            result = '{} ({})'.format(self.target.name, instruments)
        result = [result]
        return result

    @property
    def target_class(self):
        return scoretools.Performer

    ### PUBLIC METHODS ###

    def add_instruments_interactively(self):
        editor = self.InstrumentEditor(session=self.session)
        instruments = editor.select_instruments_from_instrumenttools_interactively()
        if instruments is not None:
            for instrument in instruments:
                self.target.instruments.append(instrument)

    def delete_instruments_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_argument_range('instruments', self.instrument_names)
        result = getter.run()
        if self.backtrack():
            return
        instrument_indices = [x - 1 for x in result]
        instruments = self.target.instruments
        instruments = sequencetools.remove_sequence_elements_at_indices(instruments, instrument_indices)
        self.target.instruments[:] = instruments
    
    def edit_name_interactively(self):
        if self.target.name is None:
            spaced_variable_name = 'performer name'
        else:
            spaced_variable_name = 'new performer name'
        getter = self.make_new_getter(where=self.where())
        getter.append_string_or_none(spaced_variable_name)
        result = getter.run()
        if self.backtrack():
            return
        self.target.name = result

    def handle_main_menu_response(self, key):
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        if key == 'add':
            self.add_instruments_interactively()
        elif key == 'del':
            self.delete_instruments_interactively()
        elif key == 'mv':
            self.move_instrument_interactively()
        elif key in ('name', 'ren'):
            self.edit_name_interactively()
        else:
            self.edit_instrument_interactively(key)

    def edit_instrument_interactively(self, instrument_number):
        try:
            instrument_number = int(instrument_number)
        except:
            return
        if self.target.instrument_count < instrument_number:
            message = 'there is no instrument number {}'.format(instrument_number)
            self.conditionally_display_cap_lines([message, ''])
            self.proceed()
            return
        instrument_index = instrument_number - 1
        instrument = self.target.instruments[instrument_index]
        instrument_editor = self.InstrumentEditor(session=self.session, target=instrument)
        instrument_editor.run()

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.section_title = 'instruments'
        instrument_names = [x.instrument_name for x in self.target.instruments]
        section.menu_entry_tuples = [('', x) for x in instrument_names]
        section.number_menu_entries = True
        section = menu.make_new_section()
        section.menu_entry_tuples.append(('add', 'add instruments'))
        if 0 < self.target.instrument_count:
            section.menu_entry_tuples.append(('del', 'delete instruments'))
        if 1 < self.target.instrument_count:
            section.menu_entry_tuples.append(('mv', 'move instrument'))
        if self.target.name is None:
            section.menu_entry_tuples.append(('name', 'name performer'))
        else:
            section.menu_entry_tuples.append(('ren', 'rename performer'))
        section.display_keys = False
        return menu

    def move_instrument_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_in_closed_range('old instrument number', 1, self.target.instrument_count)
        getter.append_integer_in_closed_range('new instrument number', 1, self.target.instrument_count)
        result = getter.run()
        if self.backtrack():
            return
        old_instrument_number, new_instrument_number = result
        old_instrument_index, new_instrument_index = old_instrument_number - 1, new_instrument_number - 1
        instrument = self.target.instruments[old_instrument_index]
        self.target.instruments.remove(instrument)
        self.target.instruments.insert(new_instrument_index, instrument)

    def set_initial_configuration_menu(self):
        menu, section = self.make_new_menu(where=self.where()) 
        section.allow_argument_range = True
        section.section_title = 'select instruments'
        likely_instruments = self.target.likely_instruments_based_on_performer_name
        likely_instrument_names = [x().instrument_name for x in likely_instruments]
        most_likely_instrument = self.target.most_likely_instrument_based_on_performer_name
        if most_likely_instrument is not None:
            most_likely_instrument_name = most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = '{} (default)'.format(most_likely_instrument_name)
            most_likely_number = most_likely_index + 1
            section.default_index = most_likely_index
        if likely_instruments:
            section.menu_entry_tuples = [('', x) for x in likely_instrument_names]
            section.number_menu_entries = True
            section = menu.make_new_section()
            section.menu_entry_tuples.append(('other', 'other instruments'))
        else:
            section.menu_entry_tuples = [('', x) for x in instrumenttools.list_instrument_names()]
            section.number_menu_entries = True
            section = menu.make_new_section()
        section.menu_entry_tuples.append(('none', 'no instruments'))
        section.display_keys = False
        return menu

    def set_initial_configuration_interactively(self):
        self.conditionally_initialize_target()
        self.breadcrumbs.append(self.target.name)
        menu = self.set_initial_configuration_menu()
        while True:
            key = menu.run()
            if self.backtrack():
                self.breadcrumbs.pop()
                return
            elif not key:
                continue
            #elif self.is_argument_range_string(key):
            if isinstance(key, list):
                assert isinstance(key, list)
                for instrument_name in key:
                    instrument_class = instrumenttools.default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    self.target.instruments.append(instrument)
                break
            elif key == 'none':
                break
            elif key == 'other':
                editor = self.InstrumentEditor(session=self.session)
                instruments = editor.select_instruments_from_instrumenttools_interactively()
                if instruments is not None:
                    for instrument in instruments:
                        self.target.instruments.append(instrument)
                break
            else:
                break
        self.breadcrumbs.pop()
