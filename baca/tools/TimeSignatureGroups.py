# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad import *


class TimeSignatureGroups(abctools.AbjadObject):
    r'''Time signature groups.

    ..  container:: example

        ::

            >>> import baca

    ..  container:: example

        **Example 1.** Time signature groups:

        ::

            >>> group_1 = [(3, 8), (3, 16), (3, 16)]
            >>> group_1 = [TimeSignature(_) for _ in group_1]
            >>> group_2 = [(5, 8), (5, 16), (5, 16), (5, 16)]
            >>> group_2 = [TimeSignature(_) for _ in group_2]
            >>> groups = [group_1, group_2]
            >>> groups = baca.tools.TimeSignatureGroups(groups)

        ::

            >>> print(format(groups, 'storage'))
            baca.tools.TimeSignatureGroups(
                [
                    [
                        indicatortools.TimeSignature((3, 8)),
                        indicatortools.TimeSignature((3, 16)),
                        indicatortools.TimeSignature((3, 16)),
                        ],
                    [
                        indicatortools.TimeSignature((5, 8)),
                        indicatortools.TimeSignature((5, 16)),
                        indicatortools.TimeSignature((5, 16)),
                        indicatortools.TimeSignature((5, 16)),
                        ],
                    ]
                )

        ::

            >>> show(groups) # doctest: +SKIP

    '''

    ### INITIALIZER ###

    def __init__(self, groups):
        prototype = indicatortools.TimeSignature
        for group in groups:
            assert all(isinstance(_, prototype) for _ in group), repr(group)
        self.groups = groups

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates time signature groups.

        ::

            >>> show(groups) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = groups.__illustrate__()
            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \new Score \with {
                proportionalNotationDuration = #(ly:make-moment 1 8)
            } <<
                \new Staff \with {
                    \consists Horizontal_bracket_engraver
                    \override Clef #'stencil = ##f
                    \override HorizontalBracket #'bracket-flare = #'(0 . 0)
                    \override HorizontalBracket #'direction = #up
                    \override HorizontalBracket #'extra-offset = #'(-4 . 0)
                    \override HorizontalBracket #'staff-padding = #2.5
                    \override Rest #'transparent = ##t
                    \override TextScript #'extra-offset = #'(-4 . 0)
                    \override TextScript #'staff-padding = #4.5
                } {
                    {
                        \time 3/8
                        r1 * 3/8 \startGroup
                            ^ \markup {
                                \circle
                                    \smaller
                                        0
                                }
                    }
                    {
                        \time 3/16
                        r1 * 3/16
                    }
                    {
                        \time 3/16
                        r1 * 3/16 \stopGroup
                    }
                    {
                        \time 5/8
                        r1 * 5/8 \startGroup
                            ^ \markup {
                                \circle
                                    \smaller
                                        1
                                }
                    }
                    {
                        \time 5/16
                        r1 * 5/16
                    }
                    {
                        \time 5/16
                        r1 * 5/16
                    }
                    {
                        \time 5/16
                        r1 * 5/16 \stopGroup
                    }
                }
            >>

        ::

            >>> note = Note("c'4")
            >>> show(note) # doctest: +SKIP

        Returns LilyPond file.
        ''' 
        staff = Staff()
        staff.consists_commands.append('Horizontal_bracket_engraver')
        for group_index, group in enumerate(self.groups):
            measure_group = self._make_measure_group(group)
            spanner = spannertools.HorizontalBracketSpanner()
            attach(spanner, measure_group)
            staff.extend(measure_group)
            markup = Markup(group_index, direction=Up)
            markup = markup.smaller()
            markup = markup.circle()
            attach(markup, measure_group[0])
        slide = -4
        override(staff).clef.stencil = False
        override(staff).horizontal_bracket.bracket_flare = (0, 0)
        override(staff).horizontal_bracket.direction = Up
        override(staff).horizontal_bracket.extra_offset = (slide, 0)
        override(staff).horizontal_bracket.staff_padding = 2.5
        override(staff).rest.transparent = True
        override(staff).text_script.extra_offset = (slide, 0)
        override(staff).text_script.staff_padding = 4.5
        score = Score([staff])
        moment = schemetools.SchemeMoment((1, 8))
        set_(score).proportional_notation_duration = moment
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.header_block.tagline = markuptools.Markup.null()
        return lilypond_file


    ### PRIVATE METHODS ###

    def _make_measure_group(self, group):
        measure_group = []
        for time_signature in group:
            multiplier = Multiplier(time_signature.duration)
            rest = Rest(Duration(1))
            attach(multiplier, rest)
            measure = Measure(time_signature, [rest])
            measure.always_format_time_signature = True
            measure_group.append(measure)
        return measure_group