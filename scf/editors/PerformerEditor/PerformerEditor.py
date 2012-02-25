from abjad.tools import instrumenttools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.InstrumentEditor import InstrumentEditor


class PerformerEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_class = scoretools.Performer

    ### READ-ONLY PUBLIC ATTRIBUTES ###

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
            result = '{}: no instruments'.format(self.target.name)
        elif len(self.target.instruments) == 1 and self.target.name == \
            self.target.instruments[0].instrument_name:
            result = '{}'.format(self.target.name)
        else:
            instruments = ', '.join(self.instrument_names)
            result = '{}: {}'.format(self.target.name, instruments)
        result = [result]
        return result

    ### PUBLIC METHODS ###

    def add_instruments_interactively(self):
        editor = InstrumentEditor(session=self.session)
        instruments = editor.select_instruments_from_instrumenttools_interactively()
        if instruments is not None:
            for instrument in instruments:
                self.target.instruments.append(instrument)

    def remove_instruments_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_argument_range('instruments', self.instrument_names)
        result = getter.run()
        if self.backtrack():
            return
        instrument_indices = [x - 1 for x in result]
        instruments = self.target.instruments
        instruments = sequencetools.remove_sequence_elements_at_indices(instruments, instrument_indices)
        self.target.instruments[:] = instruments
    
    def edit_instrument_interactively(self, instrument_number):
        try:
            instrument_number = int(instrument_number)
        except:
            return
        if self.target.instrument_count < instrument_number:
            line = 'there is no instrument number {}'.format(instrument_number)
            self.proceed(line)
            return
        instrument_index = instrument_number - 1
        instrument = self.target.instruments[instrument_index]
        instrument_editor = InstrumentEditor(session=self.session, target=instrument)
        instrument_editor.run()

    def edit_name_interactively(self):
        if self.target.name is None:
            spaced_variable_name = 'performer name'
        else:
            spaced_variable_name = 'new performer name'
        getter = self.make_getter(where=self.where())
        getter.append_string_or_none(spaced_variable_name)
        result = getter.run()
        if self.backtrack():
            return
        self.target.name = result

    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'add':
            self.add_instruments_interactively()
        elif result == 'rm':
            self.remove_instruments_interactively()
        elif result == 'mv':
            self.move_instrument_interactively()
        elif result in ('name', 'ren'):
            self.edit_name_interactively()
        else:
            self.edit_instrument_interactively(result)

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.return_value_attribute = 'number'
        section.title = 'instruments'
        instrument_names = [x.instrument_name for x in self.target.instruments]
        section.tokens = instrument_names
        section = menu.make_section(is_keyed=False)
        section.append(('add', 'add instruments'))
        if 0 < self.target.instrument_count:
            section.append(('rm', 'delete instruments'))
        if 1 < self.target.instrument_count:
            section.append(('mv', 'move instrument'))
        if self.target.name is None:
            section.append(('name', 'name performer'))
        else:
            section.append(('ren', 'rename performer'))
        return menu

    def move_instrument_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_integer_in_range('old instrument number', 1, self.target.instrument_count)
        getter.append_integer_in_range('new instrument number', 1, self.target.instrument_count)
        result = getter.run()
        if self.backtrack():
            return
        old_instrument_number, new_instrument_number = result
        old_instrument_index, new_instrument_index = old_instrument_number - 1, new_instrument_number - 1
        instrument = self.target.instruments[old_instrument_index]
        self.target.instruments.remove(instrument)
        self.target.instruments.insert(new_instrument_index, instrument)

    def set_initial_configuration_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        self.conditionally_initialize_target()
        menu = self.set_initial_configuration_menu()
        while True:
            self.push_breadcrumb(self.target.name)
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            if isinstance(result, list):
                for instrument_name in result:
                    instrument_class = instrumenttools.default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    self.target.instruments.append(instrument)
                break
            elif result == 'none':
                break
            elif result == 'other':
                editor = InstrumentEditor(session=self.session)
                instruments = editor.select_instruments_from_instrumenttools_interactively()
                if instruments is not None:
                    for instrument in instruments:
                        self.target.instruments.append(instrument)
                break
            else:
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def set_initial_configuration_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_ranged=True) 
        section.title = 'select instruments'
        likely_instruments = self.target.likely_instruments_based_on_performer_name
        likely_instrument_names = [x().instrument_name for x in likely_instruments]
        most_likely_instrument = self.target.most_likely_instrument_based_on_performer_name
        default_index = None
        if most_likely_instrument is not None:
            most_likely_instrument_name = most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = '{} (default)'.format(most_likely_instrument_name)
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            section.tokens = likely_instrument_names
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
            section.append(('other', 'other instruments'))
        else:
            section.tokens = instrumenttools.list_instrument_names()
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
        section.append(('none', 'no instruments'))
        return menu
