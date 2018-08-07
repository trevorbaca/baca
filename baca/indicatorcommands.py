import abjad
import typing
from . import commands
from . import indicators
from . import markups
from . import scoping
from . import typings


### FACTORY FUNCTIONS ###

def accent(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches accent.

    ..  container:: example

        Attaches accent to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \accent                                                                %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches accent to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.accent(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \accent                                                                %! IndicatorCommand
                            [
                            e''16
                            - \accent                                                                %! IndicatorCommand
                            ]
                            ef''4
                            - \accent                                                                %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \accent                                                                %! IndicatorCommand
                            [
                            g''16
                            - \accent                                                                %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('>')],
        selector=selector,
        )

def alternate_bow_strokes(
    *,
    downbow_first: bool = True,
    selector: typings.Selector = 'baca.pheads()',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches alternate bow strokes.

    :param downbow_first: is true when first stroke is down-bow.

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (down-bow first):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.alternate_bow_strokes(downbow_first=True),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \downbow                                                               %! IndicatorCommand
                            [
                            d'16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            - \downbow                                                               %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            e''16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                            ef''4
                            - \upbow                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \downbow                                                               %! IndicatorCommand
                            [
                            g''16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            - \downbow                                                               %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (up-bow first):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.alternate_bow_strokes(downbow_first=False),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(6),
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
                            \override TupletBracket.staff-padding = #6                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            d'16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                            bf'4
                            - \upbow                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            - \downbow                                                               %! IndicatorCommand
                            [
                            e''16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            - \downbow                                                               %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            g''16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            - \upbow                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.alternate_bow_strokes(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(6),
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
                            \override TupletBracket.staff-padding = #6                               %! OverrideCommand(1)
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
                            - \downbow                                                               %! IndicatorCommand
                            [
                            e''16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            - \downbow                                                               %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            g''16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    if downbow_first:
        strings = ['downbow', 'upbow']
    else:
        strings = ['upbow', 'downbow']
    indicators = [abjad.Articulation(_) for _ in strings]
    return commands.IndicatorCommand(
        indicators=indicators,
        selector=selector,
        )

def arpeggio(
    *,
    selector: typings.Selector = 'baca.chead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches arpeggio.

    ..  container:: example

        Attaches arpeggio to chord head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.arpeggio(),
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
                            - \arpeggio                                                              %! IndicatorCommand
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

        Attaches arpeggio to last two chord heads:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.arpeggio(selector=baca.cheads()[-2:]),
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
                            <ef'' e'' fs'''>8
                            - \arpeggio                                                              %! IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <g' af''>8
                            - \arpeggio                                                              %! IndicatorCommand
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
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('arpeggio')],
        selector=selector,
        )

def articulation(
    articulation: str,
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    """
    Attaches articulation.
    """
    articulation_ = abjad.Articulation(articulation)
    return commands.IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        )

def articulations(
    articulations: typing.List,
    *,
    selector: typings.Selector = 'baca.pheads()',
    ) -> commands.IndicatorCommand:
    """
    Attaches articulations.
    """
    return commands.IndicatorCommand(
        indicators=articulations,
        selector=selector,
        )

def breathe(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> commands.IndicatorCommand:
    """
    Attaches breathe command.
    """
    breathe = abjad.LilyPondLiteral(r'\breathe', format_slot='after')
    return commands.IndicatorCommand(
        indicators=[breathe],
        selector=selector,
        )

def clef(
    clef: str = 'treble',
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    redundant: bool = None,
    ) -> commands.IndicatorCommand:
    r"""
    Attaches clef.

    ..  container:: example

        Attaches clef to leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.clef('alto'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(7),
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
                            \override TupletBracket.staff-padding = #7                               %! OverrideCommand(1)
                            \clef "alto"                                                             %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches clef to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.clef(
        ...         clef='alto',
        ...         selector=baca.tuplets()[1:2].leaf(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(7),
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
                            \override TupletBracket.staff-padding = #7                               %! OverrideCommand(1)
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
                            \clef "alto"                                                             %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    indicator = abjad.Clef(clef)
    return commands.IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        )

def double_staccato(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches double-staccato.

    ..  container:: example

        Attaches double-staccato to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.double_staccato(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \baca_staccati #2                                                      %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches double-staccato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.double_staccato(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \baca_staccati #2                                                      %! IndicatorCommand
                            [
                            e''16
                            - \baca_staccati #2                                                      %! IndicatorCommand
                            ]
                            ef''4
                            - \baca_staccati #2                                                      %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \baca_staccati #2                                                      %! IndicatorCommand
                            [
                            g''16
                            - \baca_staccati #2                                                      %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('baca_staccati #2')],
        selector=selector,
        )

def down_arpeggio(
    *,
    selector: typings.Selector = 'baca.chead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches down-arpeggio.

    ..  container:: example

        Attaches down-arpeggio to chord head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.down_arpeggio(),
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
                            \arpeggioArrowDown                                                       %! IndicatorCommand
                            <c' d' bf'>8
                            \arpeggio                                                                %! IndicatorCommand
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

        Attaches down-arpeggio to last two chord heads:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.down_arpeggio(selector=baca.cheads()[-2:]),
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
                            \arpeggioArrowDown                                                       %! IndicatorCommand
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowDown                                                       %! IndicatorCommand
                            <g' af''>8
                            \arpeggio                                                                %! IndicatorCommand
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
    return commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Down)],
        selector=selector,
        )

def down_bow(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches down-bow.

    ..  container:: example

        Attaches down-bow to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.down_bow(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \downbow                                                               %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches down-bow to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.down_bow(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \downbow                                                               %! IndicatorCommand
                            [
                            e''16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                            ef''4
                            - \downbow                                                               %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \downbow                                                               %! IndicatorCommand
                            [
                            g''16
                            - \downbow                                                               %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('downbow')],
        selector=selector,
        )

def espressivo(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches espressivo.

    ..  container:: example

        Attaches espressivo to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.espressivo(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \espressivo                                                            %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches espressivo to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.espressivo(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \espressivo                                                            %! IndicatorCommand
                            [
                            e''16
                            - \espressivo                                                            %! IndicatorCommand
                            ]
                            ef''4
                            - \espressivo                                                            %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \espressivo                                                            %! IndicatorCommand
                            [
                            g''16
                            - \espressivo                                                            %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('espressivo')],
        selector=selector,
        )

def fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches fermata.

    ..  container:: example

        Attaches fermata to first leaf:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.fermata(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            - \fermata                                                               %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.fermata(selector=baca.tuplets()[1:2].phead(0)),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \fermata                                                               %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('fermata')],
        selector=selector,
        )

def flageolet(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches flageolet.

    ..  container:: example

        Attaches flageolet to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.flageolet(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \flageolet                                                             %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches flageolet to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.flageolet(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \flageolet                                                             %! IndicatorCommand
                            [
                            e''16
                            - \flageolet                                                             %! IndicatorCommand
                            ]
                            ef''4
                            - \flageolet                                                             %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \flageolet                                                             %! IndicatorCommand
                            [
                            g''16
                            - \flageolet                                                             %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('flageolet')],
        selector=selector,
        )

def hide_black_note_heads(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> commands.IndicatorCommand:
    """
    Attaches note-head stencil false to black note-heads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.hide_black_note_heads(),
        ...     baca.make_notes()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \once \override NoteHead.transparent = ##t                               %! IndicatorCommand
                            \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            \once \override NoteHead.transparent = ##t                               %! IndicatorCommand
                            \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    string = r'\once \override NoteHead.transparent = ##t'
    literal = abjad.LilyPondLiteral(string)
    return commands.IndicatorCommand(
        indicators=[literal],
        predicate=lambda _: _.written_duration < abjad.Duration(1, 2),
        selector=selector,
        )

def laissez_vibrer(
    *,
    selector: typings.Selector  = 'baca.ptail(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.laissez_vibrer(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \laissezVibrer                                                         %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches laissez vibrer to pitched tails in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.laissez_vibrer(selector=baca.ptails()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \laissezVibrer                                                         %! IndicatorCommand
                            [
                            e''16
                            - \laissezVibrer                                                         %! IndicatorCommand
                            ]
                            ef''4
                            ~
                            ef''16
                            - \laissezVibrer                                                         %! IndicatorCommand
                            r16
                            af''16
                            - \laissezVibrer                                                         %! IndicatorCommand
                            [
                            g''16
                            - \laissezVibrer                                                         %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('laissezVibrer')],
        selector=selector,
        )

def literal(
    string: str,
    *,
    format_slot: str = 'before',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    """
    Attaches LilyPond literal.
    """
    literal = abjad.LilyPondLiteral(string, format_slot=format_slot)
    return commands.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def long_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.long_fermata(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            - \longfermata                                                           %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches long fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.long_fermata(selector=baca.tuplets()[1:2].phead(0)),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \longfermata                                                           %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('longfermata')],
        selector=selector,
        )

def marcato(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.marcato(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \marcato                                                               %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches marcato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.marcato(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \marcato                                                               %! IndicatorCommand
                            [
                            e''16
                            - \marcato                                                               %! IndicatorCommand
                            ]
                            ef''4
                            - \marcato                                                               %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \marcato                                                               %! IndicatorCommand
                            [
                            g''16
                            - \marcato                                                               %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('marcato')],
        selector=selector,
        )

def margin_markup(
    argument: str,
    *,
    alert: commands.IndicatorCommand = None,
    context: str = 'Staff',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> typing.Union[commands.IndicatorCommand, scoping.Suite]:
    r"""
    Attaches margin markup.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.margin_markup('Fl.'),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            \markup { Fl. }                                                          %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                            e'2                                                                      %! baca_make_notes
                            ^ \markup \baca-explicit-indicator-markup "[MarginMarkup]"               %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                            \markup { Fl. }                                                          %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            f'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            e'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    if isinstance(argument, (str, abjad.Markup)):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(
            context=context,
            markup=markup,
            )
    elif isinstance(argument, abjad.MarginMarkup):
        margin_markup = abjad.new(
            argument,
            context=context,
            )
    else:
        raise TypeError(argument)
    assert isinstance(margin_markup, abjad.MarginMarkup)
    command = commands.IndicatorCommand(
        indicators=[margin_markup],
        selector=selector,
        )
    if bool(alert):
        assert isinstance(alert, commands.IndicatorCommand), repr(alert)
        return scoping.Suite(command, alert)
    else:
        return command

def rehearsal_mark(
    argument: typing.Union[int, str],
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    """
    Attaches rehearsal mark.
    """
    if isinstance(argument, str):
        mark = abjad.RehearsalMark.from_string(argument)
    else:
        assert isinstance(argument, int)
        mark = abjad.RehearsalMark(number=argument)
    return commands.IndicatorCommand(
        *tweaks,
        indicators=[mark],
        selector=selector,
        )

def short_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches short fermata.

    ..  container:: example

        Attaches short fermata to first leaf:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.short_fermata(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            - \shortfermata                                                          %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches short fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.short_fermata(
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \shortfermata                                                          %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('shortfermata')],
        selector=selector,
        )

def staccatissimo(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches staccatissimo.

    ..  container:: example

        Attaches staccatissimo to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.staccatissimo(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \staccatissimo                                                         %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches staccatissimo to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.staccatissimo(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \staccatissimo                                                         %! IndicatorCommand
                            [
                            e''16
                            - \staccatissimo                                                         %! IndicatorCommand
                            ]
                            ef''4
                            - \staccatissimo                                                         %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \staccatissimo                                                         %! IndicatorCommand
                            [
                            g''16
                            - \staccatissimo                                                         %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('staccatissimo')],
        selector=selector,
        )

def staccato(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches staccato.

    ..  container:: example

        Attaches staccato to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.staccato(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \staccato                                                              %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches staccato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.staccato(selector=baca.pheads()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \staccato                                                              %! IndicatorCommand
                            [
                            e''16
                            - \staccato                                                              %! IndicatorCommand
                            ]
                            ef''4
                            - \staccato                                                              %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \staccato                                                              %! IndicatorCommand
                            [
                            g''16
                            - \staccato                                                              %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('staccato')],
        selector=selector,
        )

def staff_lines(
    n: int,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
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
        ...     'MusicVoice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \clef "percussion"                                                       %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            a4.                                                                      %! baca_make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            b4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            d'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! _comment_measure_numbers
                            e'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate


        Single-line staff with bass clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b,4.                                                                     %! baca_make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            c4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            e4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! _comment_measure_numbers
                            f4.                                                                      %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Two-line staff with percussion clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \clef "percussion"                                                       %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            a4.                                                                      %! baca_make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            b4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            d'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! _comment_measure_numbers
                            e'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

        Two-line staff with bass clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b,4.                                                                     %! baca_make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            c4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            e4.                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! _comment_measure_numbers
                            f4.                                                                      %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

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
        ...     'MusicVoice',
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
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
                >>                                                                                   %! _make_global_context
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 2                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \clef "bass"                                                             %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                            g'4.                                                                     %! baca_make_notes
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            a'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            b'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            c''4.                                                                    %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! _comment_measure_numbers
                            d''4.                                                                    %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
                    }                                                                                %! SingleStaffScoreTemplate
                >>                                                                                   %! SingleStaffScoreTemplate
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    return commands.IndicatorCommand(
        indicators=[indicators.StaffLines(line_count=n)],
        selector=selector,
        )

def start_markup(
    argument: str,
    *,
    context: str = 'Staff',
    hcenter_in: typings.Number = None,
    literal: bool = None,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    """
    Attaches start markup.
    """
    if literal is True:
        assert isinstance(argument, str), repr(argument)
        assert argument.startswith('\\'), repr(argument)
        start_markup = abjad.StartMarkup(markup=argument)
    elif isinstance(argument, (list, str)):
        markup = markups.instrument(argument, hcenter_in=hcenter_in)
        start_markup = abjad.StartMarkup(
            context=context,
            markup=markup,
            )
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        start_markup = abjad.StartMarkup(
            context=context,
            markup=markup,
            )
    elif isinstance(argument, abjad.StartMarkup):
        start_markup = abjad.new(
            argument,
            context=context,
            )
    else:
        raise TypeError(argument)
    assert isinstance(start_markup, abjad.StartMarkup)
    command = commands.IndicatorCommand(
        indicators=[start_markup],
        selector=selector,
        tags=[abjad.Tag('baca_start_markup'), abjad.Tag('-PARTS')],
        )
    return command

def stem_tremolo(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    tremolo_flags:int = 32,
    ) -> commands.IndicatorCommand:
    r"""
    Attaches stem tremolo.

    ..  container:: example

        Attaches stem tremolo to pitched leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_tremolo(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            :32                                                                      %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches stem tremolo to pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.stem_tremolo(selector=baca.pleaves()),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            :32                                                                      %! IndicatorCommand
                            [
                            e''16
                            :32                                                                      %! IndicatorCommand
                            ]
                            ef''4
                            :32                                                                      %! IndicatorCommand
                            ~
                            ef''16
                            :32                                                                      %! IndicatorCommand
                            r16
                            af''16
                            :32                                                                      %! IndicatorCommand
                            [
                            g''16
                            :32                                                                      %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        )

def stop_on_string(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches stop-on-string.

    ..  container:: example

        Attaches stop-on-string to pitched head -1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.stop_on_string(selector=baca.pleaf(-1)),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            \baca_stop_on_string                                                     %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    literal = abjad.LilyPondLiteral(
        r'\baca_stop_on_string',
        format_slot='after',
        )
    return commands.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def stop_trill(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    """
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
        r'\stopTrillSpan',
        format_slot='closing',
        selector=selector,
        )

def stopped(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches stopped +-sign.

    ..  container:: example

        Attaches stopped +-sign to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.stopped(),
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \stopped                                                               %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('stopped')],
        selector=selector,
        )

def tenuto(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \tenuto                                                                %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \tenuto                                                                %! IndicatorCommand
                            [
                            e''16
                            - \tenuto                                                                %! IndicatorCommand
                            ]
                            ef''4
                            - \tenuto                                                                %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \tenuto                                                                %! IndicatorCommand
                            [
                            g''16
                            - \tenuto                                                                %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('tenuto')],
        selector=selector,
        )

def up_arpeggio(
    *,
    selector: typings.Selector = 'baca.chead(0)',
    ) -> commands.IndicatorCommand:
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
                            \arpeggioArrowUp                                                         %! IndicatorCommand
                            <c' d' bf'>8
                            \arpeggio                                                                %! IndicatorCommand
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
                            \arpeggioArrowUp                                                         %! IndicatorCommand
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! IndicatorCommand
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowUp                                                         %! IndicatorCommand
                            <g' af''>8
                            \arpeggio                                                                %! IndicatorCommand
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
    return commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Up)],
        selector=selector,
        )

def up_bow(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> commands.IndicatorCommand:
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \upbow                                                                 %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            e''16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            - \upbow                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            - \upbow                                                                 %! IndicatorCommand
                            [
                            g''16
                            - \upbow                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('upbow')],
        selector=selector,
        )

def very_long_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            - \verylongfermata                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
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
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
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
                            - \verylongfermata                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('verylongfermata')],
        selector=selector,
        )
