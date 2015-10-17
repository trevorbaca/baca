# -*- coding: utf-8 -*-
from abjad.tools import handlertools


def beam_positions(n):
    return handlertools.OverrideHandler(
        grob_name='beam',
        attribute_name='positions',
        attribute_value=str((n, n)),
        )

def cross_note_heads():
    return handlertools.OverrideHandler(
        grob_name='note_head',
        attribute_name='style',
        attribute_value="'cross'",
        )

def dynamic_line_spanner_staff_padding(n):
    return handlertools.OverrideHandler(
        grob_name='dynamic_line_spanner',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )

def markup_padding(n):
    return handlertools.OverrideHandler(
        grob_name='text_script',
        attribute_name='padding',
        attribute_value=str(n),
        )

def natural_harmonics():
    return handlertools.OverrideHandler(
        grob_name='note_head',
        attribute_name='style',
        attribute_value="'harmonic'",
        )

def repeat_tie_down():
    from abjad.tools import Down
    return handlertools.OverrideHandler(
        grob_name='repeat_tie',
        attribute_name='direction',
        attribute_value='Down',
        )

def repeat_tie_up():
    return handlertools.OverrideHandler(
        grob_name='repeat_tie',
        attribute_name='direction',
        attribute_value='Up',
        )

def stem_direction(direction):
    return handlertools.OverrideHandler(
        grob_name='stem',
        attribute_name='direction',
        attribute_value=str(direction),
        )

def text_spanner_staff_padding(n):
    return handlertools.OverrideHandler(
        grob_name='text_spanner',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )

def tie_direction(direction):
    return handlertools.OverrideHandler(
        grob_name='tie',
        attribute_name='direction',
        attribute_value=str(direction),
        )

def tuplet_bracket_down():
    return handlertools.OverrideHandler(
        grob_name='tuplet_bracket',
        attribute_name='direction',
        attribute_value=Down,
        )

def tuplet_bracket_up():
    return handlertools.OverrideHandler(
        grob_name='tuplet_bracket',
        attribute_name='direction',
        attribute_value=Up,
        )

def tuplet_bracket_staff_padding(n):
    return handlertools.OverrideHandler(
        grob_name='tuplet_bracket',
        attribute_name='staff_padding',
        attribute_value=str(n),
        )