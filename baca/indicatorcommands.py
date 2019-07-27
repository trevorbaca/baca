import abjad
import typing
from . import commands
from . import indicators
from . import markups
from . import scoping
from . import typings


### FACTORY FUNCTIONS ###


def accent(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.accent",
) -> commands.IndicatorCommand:
    r"""
    Attaches accent.

    ..  container:: example

        Attaches accent to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches accent to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.accent(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \accent                                                                %! baca.accent:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation(">")], selector=selector, tags=[tag]
    )


def alternate_bow_strokes(
    selector: abjad.SelectorTyping = "baca.pheads(exclude=abjad.const.HIDDEN)",
    *,
    downbow_first: bool = True,
    full: bool = None,
    tag: typing.Optional[str] = "baca.alternate_bow_strokes",
) -> commands.IndicatorCommand:
    r"""
    Attaches alternate bow strokes.

    :param downbow_first: is true when first stroke is down-bow.

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (down-bow first):

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=True),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (up-bow first):

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=False),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #6                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.alternate_bow_strokes:IndicatorCommand
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches alternate full bow strokes to pitched heads:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(full=True),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #6                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.alternate_bow_strokes:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.alternate_bow_strokes:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.alternate_bow_strokes:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.alternate_bow_strokes:IndicatorCommand
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    if downbow_first:
        if full:
            strings = ["baca-full-downbow", "baca-full-upbow"]
        else:
            strings = ["downbow", "upbow"]
    else:
        if full:
            strings = ["baca-full-upbow", "baca-full-downbow"]
        else:
            strings = ["upbow", "downbow"]
    indicators = [abjad.Articulation(_) for _ in strings]
    return commands.IndicatorCommand(
        indicators=indicators, selector=selector, tags=[tag]
    )


def arpeggio(
    selector: abjad.SelectorTyping = "baca.chead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.arpeggio",
) -> commands.IndicatorCommand:
    r"""
    Attaches arpeggio.

    ..  container:: example

        Attaches arpeggio to chord head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.arpeggio(),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <c' d' bf'>8
                            - \arpeggio                                                              %! baca.arpeggio:IndicatorCommand
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <g' af''>8
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches arpeggio to last two chord heads:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.arpeggio(selector=baca.cheads()[-2:]),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <ef'' e'' fs'''>8
                            - \arpeggio                                                              %! baca.arpeggio:IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <g' af''>8
                            - \arpeggio                                                              %! baca.arpeggio:IndicatorCommand
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[tag],
    )


def articulation(
    articulation: str,
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.articulation",
) -> commands.IndicatorCommand:
    """
    Attaches articulation.
    """
    articulation_ = abjad.Articulation(articulation)
    return commands.IndicatorCommand(
        indicators=[articulation_], selector=selector, tags=[tag]
    )


def articulations(
    articulations: typing.List,
    selector: abjad.SelectorTyping = "baca.pheads(exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.articulations",
) -> commands.IndicatorCommand:
    """
    Attaches articulations.
    """
    return commands.IndicatorCommand(
        indicators=articulations, selector=selector, tags=[tag]
    )


def breathe(
    selector: abjad.SelectorTyping = "baca.pleaf(-1, exclude=abjad.const.HIDDEN)",
    *tweaks: abjad.LilyPondTweakManager,
    tag: typing.Optional[str] = "baca.breathe",
) -> commands.IndicatorCommand:
    """
    Attaches breathe command.
    """
    # TODO: change to abjad.Articulation('breath', format_slot='after')?
    breathe = abjad.LilyPondLiteral(r"\breathe", format_slot="after")
    return commands.IndicatorCommand(
        indicators=[breathe], selector=selector, tags=[tag], tweaks=tweaks
    )


def clef(
    clef: str = "treble",
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    redundant: bool = None,
    tag: typing.Optional[str] = "baca.clef",
) -> commands.IndicatorCommand:
    r"""
    Attaches clef.

    ..  container:: example

        Attaches clef to leaf 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.clef('alto'),
        ...     baca.tuplet_bracket_staff_padding(7),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #7                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            \clef "alto"                                                             %! baca.clef:IndicatorCommand
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches clef to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.clef(
        ...         clef='alto',
        ...         selector=baca.tuplets()[1:2].leaf(0),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(7),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #7                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \clef "alto"                                                             %! baca.clef:IndicatorCommand
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    indicator = abjad.Clef(clef)
    return commands.IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[tag],
    )


def double_staccato(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.double_staccato",
) -> commands.IndicatorCommand:
    r"""
    Attaches double-staccato.

    ..  container:: example

        Attaches double-staccato to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.double_staccato(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches double-staccato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.double_staccato(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-staccati #2                                                      %! baca.double_staccato:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[tag],
    )


def down_arpeggio(
    selector: abjad.SelectorTyping = "baca.chead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.down_arpeggio",
) -> commands.IndicatorCommand:
    r"""
    Attaches down-arpeggio.

    ..  container:: example

        Attaches down-arpeggio to chord head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.down_arpeggio(),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowDown                                                       %! baca.down_arpeggio:IndicatorCommand
                            <c' d' bf'>8
                            \arpeggio                                                                %! baca.down_arpeggio:IndicatorCommand
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <g' af''>8
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches down-arpeggio to last two chord heads:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.down_arpeggio(selector=baca.cheads()[-2:]),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowDown                                                       %! baca.down_arpeggio:IndicatorCommand
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! baca.down_arpeggio:IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowDown                                                       %! baca.down_arpeggio:IndicatorCommand
                            <g' af''>8
                            \arpeggio                                                                %! baca.down_arpeggio:IndicatorCommand
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Down)],
        selector=selector,
        tags=[tag],
    )


def down_bow(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *tweaks: abjad.LilyPondTweakManager,
    full: bool = None,
    tag: typing.Optional[str] = "baca.down_bow",
) -> commands.IndicatorCommand:
    r"""
    Attaches down-bow.

    ..  container:: example

        Attaches down-bow to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \downbow                                                               %! baca.down_bow:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches full down-bow to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(
        ...         full=True,
        ...         selector=baca.tuplets()[1:2].pheads(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.down_bow:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.down_bow:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.down_bow:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.down_bow:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-downbow                                                     %! baca.down_bow:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    if full:
        articulation = abjad.Articulation("baca-full-downbow")
    else:
        articulation = abjad.Articulation("downbow")
    return commands.IndicatorCommand(
        indicators=[articulation], selector=selector, tags=[tag], tweaks=tweaks
    )


def espressivo(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *tweaks: abjad.LilyPondTweakManager,
    tag: typing.Optional[str] = "baca.espressivo",
) -> commands.IndicatorCommand:
    r"""
    Attaches espressivo.

    ..  container:: example

        Attaches espressivo to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.espressivo(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches espressivo to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.espressivo(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \espressivo                                                            %! baca.espressivo:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("espressivo")],
        selector=selector,
        tags=[tag],
        tweaks=tweaks,
    )


def fermata(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.fermata",
) -> commands.IndicatorCommand:
    r"""
    Attaches fermata.

    ..  container:: example

        Attaches fermata to first leaf:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.fermata(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            - \fermata                                                               %! baca.fermata:IndicatorCommand
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.fermata(selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \fermata                                                               %! baca.fermata:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[tag],
    )


def flageolet(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.flageolet",
) -> commands.IndicatorCommand:
    r"""
    Attaches flageolet.

    ..  container:: example

        Attaches flageolet to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.flageolet(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches flageolet to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.flageolet(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \flageolet                                                             %! baca.flageolet:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[tag],
    )


def hide_black_note_heads(
    selector: abjad.SelectorTyping = "baca.leaves(exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "hide.black_note_heads",
) -> commands.IndicatorCommand:
    r"""
    Attaches note-head stencil false to black note-heads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.hide_black_note_heads(),
        ...     baca.make_notes()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \once \override NoteHead.transparent = ##t                               %! hide.black_note_heads:IndicatorCommand
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \once \override NoteHead.transparent = ##t                               %! hide.black_note_heads:IndicatorCommand
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    string = r"\once \override NoteHead.transparent = ##t"
    literal = abjad.LilyPondLiteral(string)
    return commands.IndicatorCommand(
        indicators=[literal],
        predicate=lambda _: _.written_duration < abjad.Duration(1, 2),
        selector=selector,
        tags=[tag],
    )


def laissez_vibrer(
    selector: abjad.SelectorTyping = "baca.ptail(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.laissez_vibrer",
) -> commands.IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.laissez_vibrer(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs:: 

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches laissez vibrer to pitched tails in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.laissez_vibrer(selector=baca.ptails()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \laissezVibrer                                                         %! baca.laissez_vibrer:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("laissezVibrer")],
        selector=selector,
        tags=[tag],
    )


def literal(
    string: typing.Union[str, typing.List[str]],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    format_slot: str = "before",
    tag: typing.Optional[str] = "baca.literal",
) -> commands.IndicatorCommand:
    """
    Attaches LilyPond literal.
    """
    literal = abjad.LilyPondLiteral(string, format_slot=format_slot)
    return commands.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def long_fermata(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.long_fermata",
) -> commands.IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.long_fermata(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            - \longfermata                                                           %! baca.long_fermata:IndicatorCommand
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches long fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.long_fermata(selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \longfermata                                                           %! baca.long_fermata:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[tag],
    )


def marcato(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.marcato",
) -> commands.IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.marcato(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches marcato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.marcato(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \marcato                                                               %! baca.marcato:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[tag],
    )


def margin_markup(
    argument: str,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    alert: commands.IndicatorCommand = None,
    context: str = "Staff",
    tag: typing.Optional[str] = "baca.margin_markup",
) -> typing.Union[commands.IndicatorCommand, scoping.Suite]:
    r"""
    Attaches margin markup.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.margin_markup('Fl.'),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:baca.margin_markup:IndicatorCommand
                            \markup { Fl. }                                                          %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:baca.margin_markup:IndicatorCommand
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                            e'2                                                                      %! baca.make_notes
                            ^ \baca-explicit-indicator-markup "[MarginMarkup]"                       %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):baca.margin_markup:IndicatorCommand
                            \markup { Fl. }                                                          %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):baca.margin_markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            f'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'2                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    if isinstance(argument, (str, abjad.Markup)):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(context=context, markup=markup)
    elif isinstance(argument, abjad.MarginMarkup):
        margin_markup = abjad.new(argument, context=context)
    else:
        raise TypeError(argument)
    assert isinstance(margin_markup, abjad.MarginMarkup)
    command = commands.IndicatorCommand(
        indicators=[margin_markup], selector=selector, tags=[tag]
    )
    if bool(alert):
        assert isinstance(alert, commands.IndicatorCommand), repr(alert)
        return scoping.suite(command, alert)
    else:
        return command


def mark(
    argument: str,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *tweaks: abjad.LilyPondTweakManager,
    tag: typing.Optional[str] = "baca.mark",
) -> commands.IndicatorCommand:
    """
    Attaches mark.
    """
    assert isinstance(argument, (abjad.Markup, str)), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    return commands.IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[tag],
        tweaks=tweaks,
    )


def parenthesize(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.parenthesize",
) -> commands.IndicatorCommand:
    r"""
    Attaches LilyPond ``\parenthesize`` command.

    ..  container:: example

        Attaches parenthesize command to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.parenthesize(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            \parenthesize                                                            %! baca.parenthesize:IndicatorCommand
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\parenthesize")],
        selector=selector,
        tags=[tag],
    )


def quadruple_staccato(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.quadruple_staccato",
) -> commands.IndicatorCommand:
    """
    Attaches quadruple-staccato.
    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark(
    argument: typing.Union[int, str],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *tweaks: abjad.LilyPondTweakManager,
    tag: typing.Optional[str] = "baca.rehearsal_mark",
) -> commands.IndicatorCommand:
    """
    Attaches rehearsal mark.
    """
    assert isinstance(argument, str), repr(argument)
    string = rf'\baca-rehearsal-mark-markup "{argument}"'
    markup = abjad.Markup(string, direction=abjad.Center, literal=True)
    return commands.IndicatorCommand(
        indicators=[markup], selector=selector, tags=[tag], tweaks=tweaks
    )


def repeat_tie(
    selector: abjad.SelectorTyping,
    *,
    allow_rest: bool = None,
    tag: typing.Optional[str] = "baca.repeat_tie",
) -> commands.IndicatorCommand:
    r"""
    Attaches repeat-tie.

    ..  container:: example

        Attaches repeat-tie to pitched head 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(0, selector=baca.plt(1)),
        ...         baca.repeat_tie(baca.phead(1)),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            c'16                                                                     %! baca.MusicMaker.__call__
                            \repeatTie                                                               %! baca.repeat_tie:IndicatorCommand
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return commands.IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[tag],
    )


def short_fermata(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "short.fermata",
) -> commands.IndicatorCommand:
    r"""
    Attaches short fermata.

    ..  container:: example

        Attaches short fermata to first leaf:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.short_fermata(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            - \shortfermata                                                          %! short.fermata:IndicatorCommand
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches short fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.short_fermata(
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \shortfermata                                                          %! short.fermata:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[tag],
    )


def staccatissimo(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.staccatissimo",
) -> commands.IndicatorCommand:
    r"""
    Attaches staccatissimo.

    ..  container:: example

        Attaches staccatissimo to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccatissimo(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches staccatissimo to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.staccatissimo(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \staccatissimo                                                         %! baca.staccatissimo:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[tag],
    )


def staccato(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.staccato",
) -> commands.IndicatorCommand:
    r"""
    Attaches staccato.

    ..  container:: example

        Attaches staccato to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccato(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches staccato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.staccato(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \staccato                                                              %! baca.staccato:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[tag],
    )


def staff_lines(
    n: int,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.staff_lines",
) -> commands.IndicatorCommand:
    r"""
    Makes staff line command.

    ..  container:: example

        Single-line staff with percussion clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \clef "percussion"                                                       %! EXPLICIT_CLEF:_set_status_tag:baca.clef:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):baca.clef:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            a4.                                                                      %! baca.make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            b4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            e'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__


        Single-line staff with bass clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:baca.clef:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):baca.clef:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b,4.                                                                     %! baca.make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            f4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    ..  container:: example

        Two-line staff with percussion clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \clef "percussion"                                                       %! EXPLICIT_CLEF:_set_status_tag:baca.clef:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):baca.clef:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            a4.                                                                      %! baca.make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            b4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            e'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

        Two-line staff with bass clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:baca.clef:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):baca.clef:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b,4.                                                                     %! baca.make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            f4.                                                                      %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    ..  container:: example

        ..  note:: It is currently necessary to make sure that clef
            commands precede staff position commands. Otherwise output like
            the following can result:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.suite(
        ...         baca.staff_positions([-2, -1, 0, 1, 2]),
        ...         baca.clef('bass'),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:baca.clef:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):baca.clef:IndicatorCommand
                            g'4.                                                                     %! baca.make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b'4.                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c''4.                                                                    %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            d''4.                                                                    %! baca.make_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return commands.IndicatorCommand(
        indicators=[indicators.StaffLines(line_count=n)],
        selector=selector,
        tags=[tag],
    )


def start_markup(
    argument: typing.Union[str, typing.List[str]],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Staff",
    hcenter_in: abjad.Number = None,
    literal: bool = None,
    tag: typing.Optional[str] = "baca.start_markup",
) -> commands.IndicatorCommand:
    """
    Attaches start markup.
    """
    if literal is True or (
        isinstance(argument, str) and argument.startswith("\\")
    ):
        assert isinstance(argument, str), repr(argument)
        assert argument.startswith("\\"), repr(argument)
        start_markup = abjad.StartMarkup(markup=argument)
    elif isinstance(argument, (list, str)):
        markup = markups.instrument(argument, hcenter_in=hcenter_in)
        start_markup = abjad.StartMarkup(markup=markup)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        start_markup = abjad.StartMarkup(markup=markup)
    elif isinstance(argument, abjad.StartMarkup):
        start_markup = argument
    else:
        raise TypeError(argument)
    assert isinstance(start_markup, abjad.StartMarkup)
    start_markup = abjad.new(start_markup, context=context)
    command = commands.IndicatorCommand(
        indicators=[start_markup],
        selector=selector,
        tags=[tag, abjad.Tag("baca_start_markup"), abjad.Tag("-PARTS")],
    )
    return command


def stem_tremolo(
    selector: abjad.SelectorTyping = "baca.pleaf(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.stem_tremolo",
    tremolo_flags: int = 32,
) -> commands.IndicatorCommand:
    r"""
    Attaches stem tremolo.

    ..  container:: example

        Attaches stem tremolo to pitched leaf 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_tremolo(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches stem tremolo to pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.stem_tremolo(selector=baca.pleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            :32                                                                      %! baca.stem_tremolo:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[tag],
    )


def stop_on_string(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.stop_on_string",
) -> commands.IndicatorCommand:
    r"""
    Attaches stop-on-string.

    ..  container:: example

        Attaches stop-on-string to pitched head -1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stop_on_string(selector=baca.pleaf(-1)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            - \baca-stop-on-string                                                   %! baca.stop_on_string:IndicatorCommand
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    articulation = abjad.Articulation("baca-stop-on-string")
    return commands.IndicatorCommand(
        indicators=[articulation], selector=selector, tags=[tag]
    )


def stop_trill(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.stop_trill",
) -> commands.IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile
    when ``\stopTrillSpan`` appears after ``\set instrumentName`` commands
    (and probably other ``\set`` commands). Setting format slot to closing
    here positions ``\stopTrillSpan`` after the leaf in question (which is
    required) and also draws ``\stopTrillSpan`` closer to the leaf in
    question, prior to ``\set instrumetName`` and other commands positioned
    in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan``
    with a dedicated format slot.
    """
    return literal(
        r"\stopTrillSpan", format_slot="closing", selector=selector, tag=tag
    )


def stopped(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.stoppped",
) -> commands.IndicatorCommand:
    r"""
    Attaches stopped +-sign.

    ..  container:: example

        Attaches stopped +-sign to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stopped(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \stopped                                                               %! baca.stoppped:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[tag],
    )


def tie(
    selector: abjad.SelectorTyping, *, tag: typing.Optional[str] = "baca.tie"
) -> commands.IndicatorCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches tie to pitched tail 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(2, selector=baca.plt(0)),
        ...         baca.tie(baca.ptail(0)),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            d'16                                                                     %! baca.MusicMaker.__call__
                            [
                            ~                                                                        %! baca.tie:IndicatorCommand
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Tie()], selector=selector, tags=[tag]
    )


def tenuto(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.tenuto",
) -> commands.IndicatorCommand:
    r"""
    Attaches tenuto.

    ..  container:: example

        Attaches tenuto to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tenuto(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches tenuto to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.tenuto(selector=baca.pheads()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \tenuto                                                                %! baca.tenuto:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[tag],
    )


def triple_staccato(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.triple_staccato",
) -> commands.IndicatorCommand:
    """
    Attaches triple-staccato.
    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[tag],
    )


def up_arpeggio(
    selector: abjad.SelectorTyping = "baca.chead(0, exclude=abjad.const.HIDDEN)",
    *,
    tag: typing.Optional[str] = "baca.up_arpeggio",
) -> commands.IndicatorCommand:
    r"""
    Attaches up-arpeggio.

    ..  container:: example

        Attaches up-arpeggios to chord head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.up_arpeggio(),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowUp                                                         %! baca.up_arpeggio:IndicatorCommand
                            <c' d' bf'>8
                            \arpeggio                                                                %! baca.up_arpeggio:IndicatorCommand
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <g' af''>8
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches up-arpeggios to last two chord heads:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.up_arpeggio(selector=baca.cheads()[-2:]),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            f''8                                                                     %! baca.MusicMaker.__call__
                            ~
                            [
                            f''32                                                                    %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowUp                                                         %! baca.up_arpeggio:IndicatorCommand
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! baca.up_arpeggio:IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            \arpeggioArrowUp                                                         %! baca.up_arpeggio:IndicatorCommand
                            <g' af''>8
                            \arpeggio                                                                %! baca.up_arpeggio:IndicatorCommand
                            ~
                            [
                            <g' af''>32
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \scaleDurations #'(1 . 1) {                                                  %! baca.MusicMaker.__call__
                            a'8                                                                      %! baca.MusicMaker.__call__
                            ~
                            [
                            a'32                                                                     %! baca.MusicMaker.__call__
                            ]
                            r16.                                                                     %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Up)],
        selector=selector,
        tags=[tag],
    )


def up_bow(
    selector: abjad.SelectorTyping = "baca.phead(0, exclude=abjad.const.HIDDEN)",
    *tweaks: abjad.LilyPondTweakManager,
    full: bool = None,
    tag: typing.Optional[str] = "baca.up_bow",
) -> commands.IndicatorCommand:
    r"""
    Attaches up-bow.

    ..  container:: example

        Attaches up-bow to pitched head 0:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.up_bow(),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            - \upbow                                                                 %! baca.up_bow:IndicatorCommand
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches full up-bow to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.up_bow(
        ...         full=True,
        ...         selector=baca.tuplets()[1:2].pheads(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.up_bow:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.up_bow:IndicatorCommand
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.up_bow:IndicatorCommand
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.up_bow:IndicatorCommand
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            - \baca-full-upbow                                                       %! baca.up_bow:IndicatorCommand
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    if full:
        articulation = abjad.Articulation("baca-full-upbow")
    else:
        articulation = abjad.Articulation("upbow")
    return commands.IndicatorCommand(
        indicators=[articulation], selector=selector, tags=[tag], tweaks=tweaks
    )


def very_long_fermata(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.very_long_fermata",
) -> commands.IndicatorCommand:
    r"""
    Attaches very long fermata.

    ..  container:: example

        Attaches very long fermata to first leaf:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.very_long_fermata(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            - \verylongfermata                                                       %! baca.very_long_fermata:IndicatorCommand
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    ..  container:: example

        Attaches very long fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.very_long_fermata(
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {                                                                                %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            \override TupletBracket.staff-padding = #5                               %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8                                                                       %! baca.MusicMaker.__call__
                            c'16                                                                     %! baca.MusicMaker.__call__
                            [
                            d'16                                                                     %! baca.MusicMaker.__call__
                            ]
                            bf'4                                                                     %! baca.MusicMaker.__call__
                            ~
                            bf'16                                                                    %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                        \tweak text #tuplet-number::calc-fraction-text                               %! baca.MusicMaker.__call__
                        \times 9/10 {                                                                %! baca.MusicMaker.__call__
                            fs''16                                                                   %! baca.MusicMaker.__call__
                            - \verylongfermata                                                       %! baca.very_long_fermata:IndicatorCommand
                            [
                            e''16                                                                    %! baca.MusicMaker.__call__
                            ]
                            ef''4                                                                    %! baca.MusicMaker.__call__
                            ~
                            ef''16                                                                   %! baca.MusicMaker.__call__
                            r16                                                                      %! baca.MusicMaker.__call__
                            af''16                                                                   %! baca.MusicMaker.__call__
                            [
                            g''16                                                                    %! baca.MusicMaker.__call__
                            ]
                        }                                                                            %! baca.MusicMaker.__call__
                        \times 4/5 {                                                                 %! baca.MusicMaker.__call__
                            a'16                                                                     %! baca.MusicMaker.__call__
                            r4                                                                       %! baca.MusicMaker.__call__
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        }                                                                            %! baca.MusicMaker.__call__
                    }                                                                                %! baca.MusicMaker.__call__
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[tag],
    )
