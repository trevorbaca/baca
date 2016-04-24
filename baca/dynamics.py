# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.topleveltools import new


def make_ancora_dynamic(dynamic_name, direction=Down):
    markup = markuptools.Markup(dynamic_name).dynamic()
    markup += markuptools.Markup('ancora').upright()
    markup = new(markup, direction=direction)
    return markup

def make_dynamic(dynamic_name, direction=Down):
    markup = markuptools.Markup(dynamic_name, direction=direction).dynamic()
    return markup

def make_effort_dynamic(dynamic_name, direction=Down):
    # overriding font-name to false makes sure that
    # the LilyPond \dynamic command works correctly
    # in the case that TextScript.font-name is overridden score-globally
    left_quotes = markuptools.Markup('“').italic().larger()
    dynamic_markup = markuptools.Markup(dynamic_name)
    dynamic_markup = dynamic_markup.override(('font-name', False))
    dynamic_markup = dynamic_markup.dynamic()
    right_quotes = markuptools.Markup('”').italic().larger()
    markup = left_quotes + dynamic_markup + right_quotes
    markup = new(markup, direction=direction)
    return markup

def make_hairpins(
    hairpin_tokens, 
    enchain_hairpins=None,
    flare=None,
    include_following_rests=None,
    omit_lone_note_dynamic=None,
    span='contiguous notes and chords',
    ):
    import baca
    hairpin_tokens_ = []
    for hairpin_token in hairpin_tokens:
        if isinstance(hairpin_token, str):
            hairpin_token = hairpin_token.split()
            hairpin_token = tuple(hairpin_token)
        hairpin_tokens_.append(hairpin_token)
    hairpin_tokens = hairpin_tokens_
    return baca.tools.HairpinHandler(
        enchain_hairpins=enchain_hairpins,
        flare=flare,
        hairpin_tokens=hairpin_tokens,
        include_following_rests=include_following_rests,
        omit_lone_note_dynamic=omit_lone_note_dynamic,
        span=span,
        )

def make_niente_swell_specifiers(dynamics):
    import baca
    swell_specifiers = []
    for dynamic in dynamics:
        start_token = 'niente < {}'
        start_token = start_token.format(dynamic)
        stop_token = '{} > niente'
        stop_token = stop_token.format(dynamic)
        swell_specifier = baca.tools.SwellSpecifier(
            start_count=2,
            start_token=start_token,
            stop_count=2,
            stop_token=stop_token,
            )
        swell_specifiers.append(swell_specifier)
    return swell_specifiers

def make_possibile_dynamic(dynamic_name, direction=Down):
    markup = markuptools.Markup(dynamic_name).dynamic()
    markup += markuptools.Markup('possibile').upright()
    markup = new(markup, direction=direction)
    return markup

def make_reiterated_dynamic(dynamic_name):
    import baca
    return baca.tools.ReiteratedDynamicHandler(
        dynamic_name=dynamic_name,
        )