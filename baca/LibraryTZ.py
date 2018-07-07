import abjad
import baca
import collections
import typing
from abjadext import rmakers
from . import library
from . import typings
from .Command import Command
from .Command import Map
from .Command import Suite
from .Expression import Expression
from .IndicatorBundle import IndicatorBundle
from .IndicatorCommand import IndicatorCommand
from .Markup import Markup
from .PiecewiseIndicatorCommand import PiecewiseIndicatorCommand
from .Selection import Selection
from .SpannerCommand import SpannerCommand
from .TieCorrectionCommand import TieCorrectionCommand
from .VoltaCommand import VoltaCommand


__documentation_section__ = '(1) Library'

def new_text_spanner(
    *items: typing.Iterable[typing.Union[str, abjad.Markup, None]],
    bookend: typing.Union[bool, int] = -1,
    leak: bool = None,
    lilypond_id: int = None,
    piece_selector: typings.Selector = 'baca.group()',
    selector: typings.Selector = 'baca.tleaves()',
    tweaks: typing.List[abjad.LilyPondTweakManager] = None,
    ) -> PiecewiseIndicatorCommand:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single-segment spanners.

        Dashed line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.new_text_spanner('pont.', '=>', 'ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_dashed_line_with_arrow                                          %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Dashed line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.new_text_spanner('pont.', '=|', 'ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_dashed_line_with_hook                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                ord.                                                 %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Solid line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.new_text_spanner('pont.', '->', 'ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Solid line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.new_text_spanner('pont.', '-|', 'ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                ord.                                                 %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Invisible lines:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.new_text_spanner('pont.', 'ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.new_text_spanner(
        ...         'A',
        ...         'B',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.new_text_spanner(
        ...         'A',
        ...         '->',
        ...         'B',
        ...         '->',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.new_text_spanner(
        ...         'A',
        ...         'B',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.new_text_spanner(
        ...         'A',
        ...         '->',
        ...         'B',
        ...         '->',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        REGRESSION. Bookended hooks are kerned:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.new_text_spanner(
        ...         'A',
        ...         '-|',
        ...         'B',
        ...         '-|',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                A                                                    %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    shape_to_style = {
        '=>': 'dashed_line_with_arrow',
        '=|': 'dashed_line_with_hook',
        '->': 'solid_line_with_arrow',
        '-|': 'solid_line_with_hook',
        }
    bundles = []
    if len(items) == 1:
        raise NotImplementedError('implement lone item')
    if lilypond_id is None:
        command = r'\stopTextSpan'
    elif lilypond_id == 1:
        command = r'\stopTextSpanOne'
    elif lilypond_id == 2:
        command = r'\stopTextSpanTwo'
    elif lilypond_id == 3:
        command = r'\stopTextSpanThree'
    else:
        raise ValueError(lilypond_id)
    stop_text_span = abjad.StopTextSpan(command=command)
    items_ = abjad.CyclicTuple(items)
    for i, item in enumerate(items_):
        if item in shape_to_style:
            continue
        if isinstance(item, str):
            string = rf'\markup \baca-left "{item}"'
            item_markup = abjad.LilyPondLiteral(string)
        else:
            item_markup = item
            assert isinstance(item_markup, abjad.Markup)
            item_markup = item_markup.upright()
        prototype = (abjad.LilyPondLiteral, abjad.Markup)
        assert isinstance(item_markup, prototype)
        style = 'invisible_line'
        if items_[i + 1] in shape_to_style:
            style = shape_to_style[items_[i + 1]]
            right_text = items_[i + 2]
        else:
            right_text = items_[i + 1]
        right_markup: typing.Union[abjad.LilyPondLiteral, abjad.Markup]
        if isinstance(right_text, str):
            if 'hook' not in style:
                string = rf'\markup \baca-right "{right_text}"'
                right_markup = abjad.LilyPondLiteral(string)
            else:
                right_markup = abjad.Markup(right_text)
                assert isinstance(right_markup, abjad.Markup)
                right_markup = right_markup.upright()
        else:
            assert isinstance(right_text, abjad.Markup)
            right_markup = right_text.upright()
        if lilypond_id is None:
            command = r'\startTextSpan'
        elif lilypond_id == 1:
            command = r'\startTextSpanOne'
        elif lilypond_id == 2:
            command = r'\startTextSpanTwo'
        elif lilypond_id == 3:
            command = r'\startTextSpanThree'
        else:
            raise ValueError(lilypond_id)
        start_text_span = abjad.StartTextSpan(
            command=command,
            left_text=item_markup,
            style=style,
            )
        if tweaks:
            library.apply_tweaks(start_text_span, tweaks)
        # kerns bookended hook
        if 'hook' in style:
            assert isinstance(right_markup, abjad.Markup)
            line = abjad.Markup.draw_line(0, -1)
            line = line.raise_(-1)
            hspace = abjad.Markup.hspace(0.75)
            right_markup = right_markup.general_align('Y', 1)
            right_markup = abjad.Markup.concat([line, hspace, right_markup])
        bookended_spanner_start = abjad.new(
            start_text_span,
            right_text=right_markup,
            )
        manager = abjad.tweak(bookended_spanner_start)
        manager.bound_details__right__stencil_align_dir_y = abjad.Center
        if 'hook' in style:
            manager.bound_details__right__padding = 1.25
        else:
            manager.bound_details__right__padding = 0.5
        bundle = IndicatorBundle(
            stop_text_span,
            start_text_span,
            bookended_spanner_start=bookended_spanner_start,
            enchained=True,
            )
        bundles.append(bundle)
    return PiecewiseIndicatorCommand(
        bookend=bookend,
        bundles=bundles,
        leak=leak,
        piece_selector=piece_selector,
        selector=selector,
        )

def transition(
    *items: typing.Iterable[typing.Union[str, abjad.Markup, None]],
    selector: typings.Selector = 'baca.tleaves()',
    tweaks: typing.List[abjad.LilyPondTweakManager] = None,
    ):
    """
    Attaches text span indicators.
    """
    items_ = []
    for item in items:
        items_.append(item)
        items_.append('=>')
    return new_text_spanner(
        *items_,
        selector=selector,
        tweaks=tweaks,
        )

def tenuto(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches tenuto.

    ..  container:: example

        Attaches tenuto to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tenuto(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\tenuto                                                                 %! IC
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches tenuto to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tenuto(selector=baca.pheads()),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\tenuto                                                                 %! IC
                            [
                            e''16
                            -\tenuto                                                                 %! IC
                            ]
                            ef''4
                            -\tenuto                                                                 %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\tenuto                                                                 %! IC
                            [
                            g''16
                            -\tenuto                                                                 %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('tenuto')],
        selector=selector,
        )

def text_spanner(
    text: typing.Union[str, abjad.Markup],
    *tweaks: abjad.LilyPondTweakManager,
    leak: bool = None,
    lilypond_id: int = None,
    right_padding: typing.Optional[typings.Number] = 1.25,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> Suite:
    r"""
    Makes text spanner command.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner(
        ...         '1/2 clt',
        ...         abjad.tweak(4).staff_padding,
        ...         selector=baca.leaves()[:7 + 1],
        ...         ),
        ...     baca.text_spanner(
        ...         'damp',
        ...         abjad.tweak(6.5).staff_padding,
        ...         lilypond_id=1,
        ...         selector=baca.leaves()[:11 + 1],
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            - \abjad_dashed_line_with_hook                                           %! IC
                            - \tweak bound-details.left.text \markup {                               %! IC
                                \concat                                                              %! IC
                                    {                                                                %! IC
                                        \upright                                                     %! IC
                                            "1/2 clt"                                                %! IC
                                        \hspace                                                      %! IC
                                            #0.5                                                     %! IC
                                    }                                                                %! IC
                                }                                                                    %! IC
                            - \tweak bound-details.right.padding 1.25                                %! IC
                            - \tweak staff-padding #4                                                %! IC
                            \startTextSpan                                                           %! IC
                            - \abjad_dashed_line_with_hook                                           %! IC
                            - \tweak bound-details.left.text \markup {                               %! IC
                                \concat                                                              %! IC
                                    {                                                                %! IC
                                        \upright                                                     %! IC
                                            damp                                                     %! IC
                                        \hspace                                                      %! IC
                                            #0.5                                                     %! IC
                                    }                                                                %! IC
                                }                                                                    %! IC
                            - \tweak bound-details.right.padding 1.25                                %! IC
                            - \tweak staff-padding #6.5                                              %! IC
                            \startTextSpanOne                                                        %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! IC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpanOne                                                         %! IC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(text, abjad.Markup):
        markup = text
    else:
        assert isinstance(text, str), repr(text)
        markup = Markup(text)
    string = format(markup)
    if 'upright' in string:
        raise Exception(f'markup already upright:\n  {markup}')
    markup = markup.upright()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, abjad.Expression)
    if lilypond_id is None:
        command = r'\startTextSpan'
    elif lilypond_id == 1:
        command = r'\startTextSpanOne'
    elif lilypond_id == 2:
        command = r'\startTextSpanTwo'
    elif lilypond_id == 3:
        command = r'\startTextSpanThree'
    else:
        raise ValueError(lilypond_id)
    start_text_span = abjad.StartTextSpan(
        command=command,
        left_text=markup,
        right_padding=right_padding,
        style='dashed_line_with_hook',
        )
    library.apply_tweaks(start_text_span, tweaks)
    selector_ = selector.leaf(0)
    start_command = IndicatorCommand(
        indicators=[start_text_span],
        selector=selector_,
        )
    if lilypond_id is None:
        command = r'\stopTextSpan'
    elif lilypond_id == 1:
        command = r'\stopTextSpanOne'
    elif lilypond_id == 2:
        command = r'\stopTextSpanTwo'
    elif lilypond_id == 3:
        command = r'\stopTextSpanThree'
    else:
        raise ValueError(lilypond_id)
    stop_text_span = abjad.StopTextSpan(
        command=command,
        leak=leak,
        )
    selector = selector.leaf(-1)
    stop_command = IndicatorCommand(
        indicators=[stop_text_span],
        selector=selector,
        )
    return library.suite(
        start_command,
        stop_command,
        )

def tie(
    *,
    repeat: typing.Union[
        bool,
        typings.IntegerPair,
        abjad.DurationInequality,
        ] = None,
    selector: typings.Selector = 'baca.qrun(0)',
    ) -> SpannerCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            ~                                                                        %! SC
                            [
                            c'16
                            ]
                            bf'4
                            ~                                                                        %! SC
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ~                                                                        %! SC
                            ]
                            e''4
                            ~                                                                        %! SC
                            e''16
                            r16
                            fs''16
                            [
                            af''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches repeat-threshold ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(repeat=(1, 8)),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            c'16
                            \repeatTie                                                               %! SC
                            ]
                            bf'4
                            bf'16
                            \repeatTie                                                               %! SC
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ]
                            e''4
                            \repeatTie                                                               %! SC
                            e''16
                            \repeatTie                                                               %! SC
                            r16
                            fs''16
                            [
                            af''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    tie = abjad.Tie(
        repeat=repeat,
        )
    return SpannerCommand(
        selector=selector,
        spanner=tie,
        )

def tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> TieCorrectionCommand:
    r"""
    Ties from leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.tie_from(selector=baca.leaf(1)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
                            ~                                                                        %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        repeat=False,
        selector=selector,
        )

def tie_repeat_pitches() -> Map:
    """
    Ties repeat pitches.
    """
    return library.map(
        baca.select().ltqruns().nontrivial(),
        tie(),
        )

def tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Ties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.tie_to(selector=baca.leaf(1)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
                            ~                                                                        %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        repeat=False,
        selector=selector,
        )

def trill_spanner(
    string: str = None,
    *,
    harmonic: bool = None,
    left_broken: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves().with_next_leaf()',
    ) -> SpannerCommand:
    r"""
    Attaches trill spanner.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.trill_spanner(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \stopTrillSpan                                                           %! SC
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.trill_spanner(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! SC
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! SC
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                        }
                        \times 4/5 {
                            a'16
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan
                            r4
                            \stopTrillSpan                                                           %! SC
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.runs(),
        ...         baca.trill_spanner(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! SC
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! SC
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \stopTrillSpan                                                           %! SC
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        equipitch run 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.qrun(0),
        ...         baca.trill_spanner(string='Eb4'),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            \pitchedTrill                                                            %! SC
                            c'16
                            [
                            \startTrillSpan ef'
                            d'16
                            ]
                            \stopTrillSpan                                                           %! SC
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.trill_spanner(string='Eb4'),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            \pitchedTrill                                                            %! SC
                            c'16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! SC
                            d'16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! SC
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! SC
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! SC
                            fs''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! SC
                            e''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! SC
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! SC
                            \pitchedTrill                                                            %! SC
                            af''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! SC
                            g''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! SC
                            a'16
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan ef'
                            r4
                            \stopTrillSpan                                                           %! SC
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill (specified by interval) to trimmed leaves
        (leaked to the right) in every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.trill_spanner(string='M2'),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            \pitchedTrill                                                            %! SC
                            c'16
                            [
                            \startTrillSpan d'
                            \pitchedTrill                                                            %! SC
                            d'16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan e'
                            \pitchedTrill                                                            %! SC
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan c''
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! SC
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! SC
                            fs''16
                            [
                            \startTrillSpan gs''
                            \pitchedTrill                                                            %! SC
                            e''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan fs''
                            \pitchedTrill                                                            %! SC
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan f''
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! SC
                            \pitchedTrill                                                            %! SC
                            af''16
                            [
                            \startTrillSpan bf''
                            \pitchedTrill                                                            %! SC
                            g''16
                            ]
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan a''
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! SC
                            a'16
                            \stopTrillSpan                                                           %! SC
                            \startTrillSpan b'
                            r4
                            \stopTrillSpan                                                           %! SC
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    if string is None:
        interval = None
        pitch = None
    else:
        try:
            interval = None
            pitch = abjad.NamedPitch(string)
        except ValueError:
            interval = abjad.NamedInterval(string)
            pitch = None
    return SpannerCommand(
        left_broken=left_broken,
        right_broken=right_broken,
        spanner=abjad.TrillSpanner(
            interval=interval,
            is_harmonic=harmonic,
            pitch=pitch,
            ),
        selector=selector,
        )

def untie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Unties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_tied_notes(),
        ...     baca.untie_to(selector=baca.leaf(2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
                            ~
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
                            ~
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        selector=selector,
        untie=True,
        )

def up_arpeggio(
    *,
    selector: typings.Selector = 'baca.chead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches up-arpeggio.

    ..  container:: example

        Attaches up-arpeggios to chord head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.up_arpeggio(),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowUp                                                         %! IC
                            <c' d' bf'>8
                            \arpeggio                                                                %! IC
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            f''8
                            ~
                            [
                            f''32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <g' af''>8
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            ~
                            [
                            a'32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches up-arpeggios to last two chord heads:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.up_arpeggio(selector=baca.cheads()[-2:]),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            f''8
                            ~
                            [
                            f''32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowUp                                                         %! IC
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! IC
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowUp                                                         %! IC
                            <g' af''>8
                            \arpeggio                                                                %! IC
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            ~
                            [
                            a'32
                            ]
                            r16.
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Up)],
        selector=selector,
        )

def up_bow(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches up-bow.

    ..  container:: example

        Attaches up-bow to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.up_bow(),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\upbow                                                                  %! IC
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches up-bow to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.up_bow(selector=baca.pheads()),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\upbow                                                                  %! IC
                            [
                            e''16
                            -\upbow                                                                  %! IC
                            ]
                            ef''4
                            -\upbow                                                                  %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! IC
                            [
                            g''16
                            -\upbow                                                                  %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('upbow')],
        selector=selector,
        )

def very_long_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches very long fermata.

    ..  container:: example

        Attaches very long fermata to first leaf:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.very_long_fermata(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            -\verylongfermata                                                        %! IC
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches very long fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.very_long_fermata(
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\verylongfermata                                                        %! IC
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('verylongfermata')],
        selector=selector,
        )

def voice_four(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceFour')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_one(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceOne')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_three(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceThree')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_two(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceTwo')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def volta(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> VoltaCommand:
    r"""
    Makes volta container and extends container with ``selector`` output.

    ..  container:: example

        Wraps stage 1 (global skips 1 and 2) in volta container:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     'GlobalSkips',
        ...     baca.volta(selector=baca.skips()[1:3]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! SM4
                            \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! SM4
                            \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Wraps stage 2 global skips in volta container:

        >>> maker = baca.SegmentMaker(
        ...     measures_per_stage=[1, 2, 1],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     ('MusicVoice', (1, 3)),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     ('GlobalSkips', 2),
        ...     baca.volta(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! SM4
                            \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! SM4
                            \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return VoltaCommand(selector=selector)
