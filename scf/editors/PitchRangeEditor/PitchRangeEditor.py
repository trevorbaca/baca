from abjad.tools import pitchtools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf import predicates


class PitchRangeEditor(InteractiveEditor):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'pitch range editor'

    target_attribute_tuples = (
        ('start_pitch', predicates.is_named_chromatic_pitch, False, None, 'sp', 'pitch_class_octave_label'),
        ('stop_pitch', predicates.is_named_chromatic_pitch, False, None, 'tp', 'pitch_class_octave_label'),
        ('start_pitch_is_included_in_range', predicates.is_boolean, False, True, 'si'),
        ('stop_pitch_is_included_in_range', predicates.is_boolean, False, True, 'ti'),
        ('pitch_range_name', predicates.is_string, False, None, 'nm'),
        ('pitch_range_name_markup', predicates.is_markup_token, False, None, 'mk'),
        )

    target_class = pitchtools.PitchRange

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            getter = self.make_getter(where=self.where())
            getter.append_symbolic_pitch_range_string('symbolic pitch range string')
            result = getter.run()
            if self.backtrack():
                return
            symbolic_pitch_range_string = result
            pitch_range = self.target_class(symbolic_pitch_range_string)
            self.target = pitch_range

    def edit_start_pitch_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_named_chromatic_pitch('start pitch')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('start_pitch', result)

    def edit_start_pitch_is_included_in_range_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_boolean('start pitch is included in range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('start_pitch_is_included_in_range', result)

    def edit_stop_pitch_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_named_chromatic_pitch('stop pitch')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('stop_pitch', result)

    def edit_stop_pitch_is_included_in_range_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_boolean('stop pitch is included in range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('stop_pitch_is_included_in_range', result)

    def handle_main_menu_result(self, result):
        if result == 'sp':
            self.edit_start_pitch_interactively()
        elif result == 'tp':
            self.edit_stop_pitch_interactively()
        elif result == 'si':
            self.edit_start_pitch_is_included_in_range_interactively()
        elif result == 'ti':
            self.edit_stop_pitch_is_included_in_range_interactively()
        elif result == 'nm':
            self.edit_pitch_range_name_interactively()
        elif result == 'mk':
            self.edit_pitch_range_name_markup_interacitvely()
        else:
            raise ValueError

    def make_main_menu(self):
        #menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_keyed=False)
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.target_attribute_tokens
        section.show_existing_values = True
        return menu
