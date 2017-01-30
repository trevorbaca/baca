# -*- coding: utf-8 -*-
import abjad
import baca
import numbers


class OverrideInterface(object):
    r'''Override interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Interfaces'

    ### PUBLIC METHODS ###

    @staticmethod
    def beam_positions(n):
        assert isinstance(n, (int, float)), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='beam',
            attribute_name='positions',
            attribute_value=str((n, n)),
            )

    @staticmethod
    def cross_note_heads():
        return baca.tools.OverrideSpecifier(
            grob_name='note_head',
            attribute_name='style',
            attribute_value="'cross'",
            )

    @staticmethod
    def dynamic_line_spanner_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='dynamic_line_spanner',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def dynamic_line_spanner_up():
        return baca.tools.OverrideSpecifier(
            grob_name='dynamic_line_spanner',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def natural_harmonics():
        return baca.tools.OverrideSpecifier(
            grob_name='note_head',
            attribute_name='style',
            attribute_value="'harmonic'",
            )

    @staticmethod
    def proportional_notation_duration(duration):
        assert isinstance(duration, tuple), repr(duration)
        assert len(duration) == 2, repr(duration)
        moment = abjad.schemetools.SchemeMoment(duration)
        return baca.tools.SettingSpecifier(
            context_name='score',
            setting_name='proportional_notation_duration',
            setting_value=moment,
            )

    @staticmethod
    def repeat_tie_down():
        return baca.tools.OverrideSpecifier(
            grob_name='repeat_tie',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def repeat_tie_up():
        return baca.tools.OverrideSpecifier(
            grob_name='repeat_tie',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def script_direction(direction):
        return baca.tools.OverrideSpecifier(
            grob_name='script',
            attribute_name='direction',
            attribute_value=str(direction),
            )

    @staticmethod
    def script_down():
        return baca.tools.OverrideSpecifier(
            grob_name='script',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def script_up():
        return baca.tools.OverrideSpecifier(
            grob_name='script',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def stem_direction(direction):
        return baca.tools.OverrideSpecifier(
            grob_name='stem',
            attribute_name='direction',
            attribute_value=str(direction),
            )

    @staticmethod
    def stem_down():
        return baca.tools.OverrideSpecifier(
            grob_name='stem',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def stem_up():
        return baca.tools.OverrideSpecifier(
            grob_name='stem',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def text_script_color(color):
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='color',
            attribute_value=repr(color),
            )

    @staticmethod
    def text_script_down():
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def text_script_padding(n):
        assert isinstance(n, numbers.Number), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='padding',
            attribute_value=n,
            )

    @staticmethod
    def text_script_staff_padding(n):
        assert isinstance(n, numbers.Number), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='staff_padding',
            attribute_value=n,
            )

    @staticmethod
    def text_script_up():
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def text_spanner_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='text_spanner',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def tie_direction(direction):
        return baca.tools.OverrideSpecifier(
            grob_name='tie',
            attribute_name='direction',
            attribute_value=str(direction),
            )

    @staticmethod
    def time_signature_extra_offset(extra_offset_pair):
        assert isinstance(extra_offset_pair, tuple), repr(extra_offset_pair)
        return baca.tools.OverrideSpecifier(
            context_name='score',
            grob_name='time_signature',
            attribute_name='extra_offset',
            attribute_value=extra_offset_pair,
            )

    @staticmethod
    def tuplet_bracket_down():
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def tuplet_bracket_extra_offset(pair):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='extra_offset',
            attribute_value=pair,
            )

    @staticmethod
    def tuplet_bracket_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def tuplet_bracket_up():
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='direction',
            attribute_value=Up,
            )
            
    @staticmethod
    def tuplet_number_extra_offset(pair):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_number',
            attribute_name='extra_offset',
            attribute_value=pair,
            )
