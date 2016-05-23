# -*- coding: utf-8 -*-
import abjad
import numbers


def beam_positions(n):
    import baca
    assert isinstance(n, (int, float)), repr(n)
    return baca.tools.OverrideSpecifier(
        grob_name='beam',
        attribute_name='positions',
        attribute_value=str((n, n)),
        )

def cross_note_heads():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='note_head',
        attribute_name='style',
        attribute_value="'cross'",
        )

def dynamic_line_spanner_staff_padding(n):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='dynamic_line_spanner',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )

def dynamic_line_spanner_up():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='dynamic_line_spanner',
        attribute_name='direction',
        attribute_value='Up',
        )

def natural_harmonics():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='note_head',
        attribute_name='style',
        attribute_value="'harmonic'",
        )

def proportional_notation_duration(duration):
    import baca
    assert isinstance(duration, tuple), repr(duration)
    assert len(duration) == 2, repr(duration)
    moment = abjad.schemetools.SchemeMoment(duration)
    return baca.tools.SettingSpecifier(
        context_name='score',
        setting_name='proportional_notation_duration',
        setting_value=moment,
        )

def repeat_tie_down():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='repeat_tie',
        attribute_name='direction',
        attribute_value='Down',
        )

def repeat_tie_up():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='repeat_tie',
        attribute_name='direction',
        attribute_value='Up',
        )

def stem_direction(direction):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='stem',
        attribute_name='direction',
        attribute_value=str(direction),
        )

def stem_down():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='stem',
        attribute_name='direction',
        attribute_value='Down',
        )

def stem_up():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='stem',
        attribute_name='direction',
        attribute_value='Up',
        )

def text_script_color(color):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='text_script',
        attribute_name='color',
        attribute_value=repr(color),
        )

def text_script_padding(n):
    import baca
    assert isinstance(n, numbers.Number), repr(n)
    return baca.tools.OverrideSpecifier(
        grob_name='text_script',
        attribute_name='padding',
        attribute_value=n,
        )

def text_script_staff_padding(n):
    import baca
    assert isinstance(n, numbers.Number), repr(n)
    return baca.tools.OverrideSpecifier(
        grob_name='text_script',
        attribute_name='staff_padding',
        attribute_value=n,
        )

def text_spanner_staff_padding(n):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='text_spanner',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )

def tie_direction(direction):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='tie',
        attribute_name='direction',
        attribute_value=str(direction),
        )

def time_signature_extra_offset(extra_offset_pair):
    import baca
    assert isinstance(extra_offset_pair, tuple), repr(extra_offset_pair)
    return baca.tools.OverrideSpecifier(
        context_name='score',
        grob_name='time_signature',
        attribute_name='extra_offset',
        attribute_value=extra_offset_pair,
        )

def tuplet_bracket_down():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='tuplet_bracket',
        attribute_name='direction',
        attribute_value=Down,
        )

def tuplet_bracket_staff_padding(n):
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='tuplet_bracket',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )

def tuplet_bracket_up():
    import baca
    return baca.tools.OverrideSpecifier(
        grob_name='tuplet_bracket',
        attribute_name='direction',
        attribute_value='Up',
        )