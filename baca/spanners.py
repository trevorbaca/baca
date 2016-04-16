# -*- coding: utf-8 -*-
import baca
from abjad.tools import durationtools
from abjad.tools import spannertools
from abjad.tools import patterntools
from abjad.tools.markuptools import Markup


def clef_spanner(clef='percussion'):
    return spannertools.ClefSpanner(clef=clef)

def five_line_staff():
    return spannertools.StaffLinesSpanner(lines=5)

def grid_poss_to_flaut_poss():
    left_text = Markup('grid. possibile').italic().larger() + Markup.hspace(1)
    right_text = Markup.hspace(1) + Markup('flaut. possibile')
    right_text = right_text.italic().larger()
    grid_poss_to_flaut_poss = spannertools.TextSpanner(
        overrides = {
            'text_spanner__bound_details__left__padding': -1,
            'text_spanner__bound_details__left__stencil_align_dir_y': 0,
            'text_spanner__bound_details__left__text': left_text,
            'text_spanner__bound_details__left_broken__text': None,
            'text_spanner__bound_details__right__arrow': True,
            'text_spanner__bound_details__right__padding': 1,
            'text_spanner__bound_details__right__stencil_align_dir_y': 0,
            'text_spanner__bound_details__right__text': right_text,
            'text_spanner__bound_details__right_broken__padding': 0,
            'text_spanner__bound_details__right_broken__text': None,
            'text_spanner__dash_fraction': 0.25,
            'text_spanner__dash_period': 1.5,
        }
    )

def glissandi():
    return baca.tools.GlissandoSpecifier(
        patterns=patterntools.select_last(1, inverted=True),
        )

def make_transition(start_markup=None, stop_markup=None):
    return baca.tools.TransitionSpecifier(
        start_markup=start_markup,
        stop_markup=stop_markup,
        )

def molto_flaut_to_molto_grid():
    left_text = Markup('molto flautando').italic().larger() + Markup.hspace(1)
    right_text = Markup.hspace(1) + Markup('molto gridato').italic().larger()
    molto_flaut_to_molto_grid = spannertools.TextSpanner(
        overrides = {
            'text_spanner__bound_details__left__padding': -1,
            'text_spanner__bound_details__left__stencil_align_dir_y': 0,
            'text_spanner__bound_details__left__text': left_text,
            'text_spanner__bound_details__left_broken__text': None,
            'text_spanner__bound_details__right__arrow': True,
            'text_spanner__bound_details__right__padding': 1,
            'text_spanner__bound_details__right__stencil_align_dir_y': 0,
            'text_spanner__bound_details__right__text': right_text,
            'text_spanner__bound_details__right_broken__padding': 0,
            'text_spanner__bound_details__right_broken__text': None,
            'text_spanner__dash_fraction': 0.25,
            'text_spanner__dash_period': 1.5,
        }
    )

def one_line_staff():
    return spannertools.StaffLinesSpanner(lines=1)

def ottava():
    return spannertools.OctavationSpanner(start=1, stop=0)

def ottava_bassa():
    return spannertools.OctavationSpanner(start=-1, stop=0)

def percussion_staff():
    return spannertools.ClefSpanner(clef='percussion')

def pervasive_trills():
    return baca.tools.TrillSpecifier(
        minimum_written_duration=None,
        )

def pervasive_trills_at_interval(interval):
    return baca.tools.TrillSpecifier(
        interval=interval,
        minimum_written_duration=None,
        )

def pervasive_trills_at_pitch(pitch, is_harmonic=None):
    return baca.tools.TrillSpecifier(
        is_harmonic=is_harmonic,
        minimum_written_duration=None,
        pitch=pitch,
        )
    
def trill_quarter_notes():
    return baca.tools.TrillSpecifier(
        forbidden_annotations=['color fingering', 'color microtone'],
        minimum_written_duration=durationtools.Duration(1, 4),
        )

def two_line_staff():
    return spannertools.StaffLinesSpanner(lines=2)