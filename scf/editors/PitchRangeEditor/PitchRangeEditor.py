from abjad.tools import pitchtools
from baca.scf.editors.InteractiveEditor import InteractiveEditor


class PitchRangeEditor(InteractiveEditor):

    ### PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'pitch range editor'

    @property
    def target_attribute_tuples(self):
        return (
            ('start_pitch', self.is_named_chromatic_pitch, False, None),
            ('start_pitch_is_included_in_range', self.is_boolean, False, True),
            ('stop_pitch', self.is_named_chromatic_pitch, False, None),
            ('stop_pitch_is_included_in_range', self.is_boolean, False, True),)

    @property
    def target_class(self):
        return pitchtools.PitchRange

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            getter = self.make_new_getter(where=self.where())
            getter.append_symbolic_pitch_range_string('symbolic pitch range string')
            result = getter.run()
            if self.backtrack():
                return
            symbolic_pitch_range_string = result
            pitch_range = self.target_class(symbolic_pitch_range_string)
            self.target = pitch_range

    def edit_start_pitch_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_named_chromatic_pitch('start pitch')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('start_pitch', result)

    def edit_start_pitch_is_included_in_range_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_boolean('start pitch is included in range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('start_pitch_is_included_in_range', result)

    def edit_stop_pitch_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_named_chromatic_pitch('stop pitch')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('stop_pitch', result)

    def edit_stop_pitch_is_included_in_range_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_boolean('stop pitch is included in range')
        result = getter.run()
        if self.backtrack():
            return
        self.conditionally_set_target_attribute('stop_pitch_is_included_in_range', result)

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tokens = self.target_attribute_menu_entry_tokens
        return menu
