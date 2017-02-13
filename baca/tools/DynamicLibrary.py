# -*- coding: utf-8 -*-
import abjad
import baca


class DynamicLibrary(object):
    r'''Dynamic interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    @staticmethod
    def dynamic_down():
        command = abjad.LilyPondCommand('dynamicDown')
        return baca.wrap.leaves(command)

    @staticmethod
    def dynamic_first_note(dynamic):
        dynamic = abjad.Dynamic(dynamic)
        prototype = (abjad.Note, abjad.Chord)
        selector = abjad.select().by_class(prototype=prototype)
        return baca.tools.DynamicSpecifier(
            dynamic=dynamic,
            selector=selector,
            )

    @staticmethod
    def dynamic_up():
        command = abjad.LilyPondCommand('dynamicUp')
        return baca.wrap.leaves(command)

    @staticmethod
    def make_ancora_dynamic(dynamic_name, direction=Down):
        markup = abjad.Markup(dynamic_name).dynamic()
        markup += abjad.Markup('ancora').upright()
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def make_dynamic(dynamic_name, direction=Down):
        markup = abjad.Markup(dynamic_name, direction=direction).dynamic()
        return markup

    @staticmethod
    def make_effort_dynamic(dynamic_name, direction=Down):
        # overriding font-name to false makes sure that
        # the LilyPond \dynamic command works correctly
        # in the case that TextScript.font-name is overridden score-globally
        left_quotes = abjad.Markup('“').italic().larger()
        dynamic_markup = abjad.Markup(dynamic_name)
        dynamic_markup = dynamic_markup.override(('font-name', False))
        dynamic_markup = dynamic_markup.dynamic()
        right_quotes = abjad.Markup('”').italic().larger()
        markup = left_quotes + dynamic_markup + right_quotes
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def make_hairpins(
        hairpin_tokens, 
        enchain_hairpins=None,
        flare=None,
        include_following_rests=None,
        omit_lone_note_dynamic=None,
        span='contiguous notes and chords',
        ):
        hairpin_tokens_ = []
        for hairpin_token in hairpin_tokens:
            if isinstance(hairpin_token, str):
                hairpin_token = hairpin_token.split()
                hairpin_token = tuple(hairpin_token)
            hairpin_tokens_.append(hairpin_token)
        hairpin_tokens = hairpin_tokens_
        return baca.tools.HairpinSpecifier(
            enchain_hairpins=enchain_hairpins,
            flare=flare,
            hairpin_tokens=hairpin_tokens,
            include_following_rests=include_following_rests,
            omit_lone_note_dynamic=omit_lone_note_dynamic,
            span=span,
            )

    @staticmethod
    def make_niente_swell_specifiers(dynamics):
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

    @staticmethod
    def make_possibile_dynamic(dynamic_name, direction=Down):
        markup = abjad.Markup(dynamic_name).dynamic()
        markup += abjad.Markup('possibile').upright()
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def make_reiterated_dynamic(dynamic_name):
        return baca.tools.ArticulationSpecifier(
            articulations=[dynamic_name],
            )
