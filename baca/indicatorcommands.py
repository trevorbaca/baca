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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\accent                                                                 %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\accent                                                                 %! INDICATOR_COMMAND
                            [
                            e''16
                            -\accent                                                                 %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\accent                                                                 %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! INDICATOR_COMMAND
                            [
                            g''16
                            -\accent                                                                 %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            d'16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                            bf'4
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            e''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            g''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #6                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            d'16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                            bf'4
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            e''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            g''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #6                               %! OVERRIDE_COMMAND_1
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
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            e''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            g''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            -\arpeggio                                                               %! INDICATOR_COMMAND
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
                            -\arpeggio                                                               %! INDICATOR_COMMAND
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <g' af''>8
                            -\arpeggio                                                               %! INDICATOR_COMMAND
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
                            \override TupletBracket.staff-padding = #7                               %! OVERRIDE_COMMAND_1
                            \clef "alto"                                                             %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #7                               %! OVERRIDE_COMMAND_1
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
                            \clef "alto"                                                             %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
                            [
                            e''16
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
                            [
                            g''16
                            -\baca_staccati #2                                                       %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \arpeggioArrowDown                                                       %! INDICATOR_COMMAND
                            <c' d' bf'>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
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
                            \arpeggioArrowDown                                                       %! INDICATOR_COMMAND
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowDown                                                       %! INDICATOR_COMMAND
                            <g' af''>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\downbow                                                                %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            e''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            [
                            g''16
                            -\downbow                                                                %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\espressivo                                                             %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\espressivo                                                             %! INDICATOR_COMMAND
                            [
                            e''16
                            -\espressivo                                                             %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\espressivo                                                             %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\espressivo                                                             %! INDICATOR_COMMAND
                            [
                            g''16
                            -\espressivo                                                             %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            -\fermata                                                                %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\fermata                                                                %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\flageolet                                                              %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\flageolet                                                              %! INDICATOR_COMMAND
                            [
                            e''16
                            -\flageolet                                                              %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\flageolet                                                              %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\flageolet                                                              %! INDICATOR_COMMAND
                            [
                            g''16
                            -\flageolet                                                              %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 4/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/2                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 4/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/2                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            \once \override NoteHead.transparent = ##t                               %! INDICATOR_COMMAND
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            \once \override NoteHead.transparent = ##t                               %! INDICATOR_COMMAND
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
                            [
                            e''16
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
                            ]
                            ef''4
                            ~
                            ef''16
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
                            r16
                            af''16
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
                            [
                            g''16
                            -\laissezVibrer                                                          %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            -\longfermata                                                            %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\longfermata                                                            %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\marcato                                                                %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\marcato                                                                %! INDICATOR_COMMAND
                            [
                            e''16
                            -\marcato                                                                %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\marcato                                                                %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\marcato                                                                %! INDICATOR_COMMAND
                            [
                            g''16
                            -\marcato                                                                %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 4/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/2                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 4/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/2                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \set Staff.instrumentName =                                              %! SET_STATUS_TAG:EXPLICIT_MARGIN_MARKUP:INDICATOR_COMMAND
                            \markup { Fl. }                                                          %! SET_STATUS_TAG:EXPLICIT_MARGIN_MARKUP:INDICATOR_COMMAND
                            \set Staff.shortInstrumentName =                                         %! SET_STATUS_TAG:EXPLICIT_MARGIN_MARKUP:INDICATOR_COMMAND
                            \markup { Fl. }                                                          %! SET_STATUS_TAG:EXPLICIT_MARGIN_MARKUP:INDICATOR_COMMAND
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! ATTACH_COLOR_LITERAL_2:EXPLICIT_MARGIN_MARKUP_COLOR:INDICATOR_COMMAND
                            e'2
                            ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:INDICATOR_COMMAND
                                \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:INDICATOR_COMMAND
                                    #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:INDICATOR_COMMAND
                                    [MarginMarkup]                                                   %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:INDICATOR_COMMAND
                                }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:INDICATOR_COMMAND
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! ATTACH_COLOR_LITERAL_2:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:INDICATOR_COMMAND
                            \set Staff.instrumentName =                                              %! SET_STATUS_TAG:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:INDICATOR_COMMAND
                            \markup { Fl. }                                                          %! SET_STATUS_TAG:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:INDICATOR_COMMAND
                            \set Staff.shortInstrumentName =                                         %! SET_STATUS_TAG:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:INDICATOR_COMMAND
                            \markup { Fl. }                                                          %! SET_STATUS_TAG:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            f'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            e'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            f'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            -\shortfermata                                                           %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\shortfermata                                                           %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
                            [
                            e''16
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
                            [
                            g''16
                            -\staccatissimo                                                          %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\staccato                                                               %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\staccato                                                               %! INDICATOR_COMMAND
                            [
                            e''16
                            -\staccato                                                               %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\staccato                                                               %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\staccato                                                               %! INDICATOR_COMMAND
                            [
                            g''16
                            -\staccato                                                               %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \stopStaff                                                               %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.line-count = 1                         %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \startStaff                                                              %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \clef "percussion"                                                       %! SET_STATUS_TAG:EXPLICIT_CLEF:INDICATOR_COMMAND
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_COLOR:INDICATOR_COMMAND
                        %@% \override Staff.Clef.color = ##f                                         %! ATTACH_COLOR_LITERAL_1:EXPLICIT_CLEF_COLOR_CANCELLATION:INDICATOR_COMMAND
                            \set Staff.forceClef = ##t                                               %! SET_STATUS_TAG:EXPLICIT_CLEF:SM33:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! ATTACH_COLOR_LITERAL_2:EXPLICIT_STAFF_LINES_COLOR:INDICATOR_COMMAND
                            a4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_REDRAW_COLOR:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            b4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            d'4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! COMMENT_MEASURE_NUMBERS
                            e'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>


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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \stopStaff                                                               %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.line-count = 1                         %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \startStaff                                                              %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \clef "bass"                                                             %! SET_STATUS_TAG:EXPLICIT_CLEF:INDICATOR_COMMAND
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_COLOR:INDICATOR_COMMAND
                        %@% \override Staff.Clef.color = ##f                                         %! ATTACH_COLOR_LITERAL_1:EXPLICIT_CLEF_COLOR_CANCELLATION:INDICATOR_COMMAND
                            \set Staff.forceClef = ##t                                               %! SET_STATUS_TAG:EXPLICIT_CLEF:SM33:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! ATTACH_COLOR_LITERAL_2:EXPLICIT_STAFF_LINES_COLOR:INDICATOR_COMMAND
                            b,4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_REDRAW_COLOR:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            c4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            d4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            e4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! COMMENT_MEASURE_NUMBERS
                            f4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \stopStaff                                                               %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \startStaff                                                              %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \clef "percussion"                                                       %! SET_STATUS_TAG:EXPLICIT_CLEF:INDICATOR_COMMAND
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_COLOR:INDICATOR_COMMAND
                        %@% \override Staff.Clef.color = ##f                                         %! ATTACH_COLOR_LITERAL_1:EXPLICIT_CLEF_COLOR_CANCELLATION:INDICATOR_COMMAND
                            \set Staff.forceClef = ##t                                               %! SET_STATUS_TAG:EXPLICIT_CLEF:SM33:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! ATTACH_COLOR_LITERAL_2:EXPLICIT_STAFF_LINES_COLOR:INDICATOR_COMMAND
                            a4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_REDRAW_COLOR:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            b4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            d'4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! COMMENT_MEASURE_NUMBERS
                            e'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \stopStaff                                                               %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \startStaff                                                              %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \clef "bass"                                                             %! SET_STATUS_TAG:EXPLICIT_CLEF:INDICATOR_COMMAND
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_COLOR:INDICATOR_COMMAND
                        %@% \override Staff.Clef.color = ##f                                         %! ATTACH_COLOR_LITERAL_1:EXPLICIT_CLEF_COLOR_CANCELLATION:INDICATOR_COMMAND
                            \set Staff.forceClef = ##t                                               %! SET_STATUS_TAG:EXPLICIT_CLEF:SM33:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! ATTACH_COLOR_LITERAL_2:EXPLICIT_STAFF_LINES_COLOR:INDICATOR_COMMAND
                            b,4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_REDRAW_COLOR:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            c4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            d4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            e4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! COMMENT_MEASURE_NUMBERS
                            f4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
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
                            % [MusicVoice measure 1]                                                 %! COMMENT_MEASURE_NUMBERS
                            \stopStaff                                                               %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \startStaff                                                              %! SET_STATUS_TAG:EXPLICIT_STAFF_LINES:INDICATOR_COMMAND
                            \clef "bass"                                                             %! SET_STATUS_TAG:EXPLICIT_CLEF:INDICATOR_COMMAND
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! ATTACH_COLOR_LITERAL_2:EXPLICIT_STAFF_LINES_COLOR:INDICATOR_COMMAND
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_COLOR:INDICATOR_COMMAND
                        %@% \override Staff.Clef.color = ##f                                         %! ATTACH_COLOR_LITERAL_1:EXPLICIT_CLEF_COLOR_CANCELLATION:INDICATOR_COMMAND
                            \set Staff.forceClef = ##t                                               %! SET_STATUS_TAG:EXPLICIT_CLEF:SM33:INDICATOR_COMMAND
                            g'4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! ATTACH_COLOR_LITERAL_2:EXPLICIT_CLEF_REDRAW_COLOR:INDICATOR_COMMAND
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! COMMENT_MEASURE_NUMBERS
                            a'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! COMMENT_MEASURE_NUMBERS
                            b'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! COMMENT_MEASURE_NUMBERS
                            c''4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! COMMENT_MEASURE_NUMBERS
                            d''4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

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
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> commands.IndicatorCommand:
    """
    Attaches start markup.
    """
    if isinstance(argument, (list, str)):
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
        tags=[abjad.Tag('STMK'), abjad.Tag('-PARTS')],
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            :32                                                                      %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            :32                                                                      %! INDICATOR_COMMAND
                            [
                            e''16
                            :32                                                                      %! INDICATOR_COMMAND
                            ]
                            ef''4
                            :32                                                                      %! INDICATOR_COMMAND
                            ~
                            ef''16
                            :32                                                                      %! INDICATOR_COMMAND
                            r16
                            af''16
                            :32                                                                      %! INDICATOR_COMMAND
                            [
                            g''16
                            :32                                                                      %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            \baca_stop_on_string                                                     %! INDICATOR_COMMAND
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\stopped                                                                %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\tenuto                                                                 %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\tenuto                                                                 %! INDICATOR_COMMAND
                            [
                            e''16
                            -\tenuto                                                                 %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\tenuto                                                                 %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\tenuto                                                                 %! INDICATOR_COMMAND
                            [
                            g''16
                            -\tenuto                                                                 %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \arpeggioArrowUp                                                         %! INDICATOR_COMMAND
                            <c' d' bf'>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
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
                            \arpeggioArrowUp                                                         %! INDICATOR_COMMAND
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowUp                                                         %! INDICATOR_COMMAND
                            <g' af''>8
                            \arpeggio                                                                %! INDICATOR_COMMAND
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            -\upbow                                                                  %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            e''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                            ef''4
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            [
                            g''16
                            -\upbow                                                                  %! INDICATOR_COMMAND
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            -\verylongfermata                                                        %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
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
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
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
                            -\verylongfermata                                                        %! INDICATOR_COMMAND
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
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('verylongfermata')],
        selector=selector,
        )
