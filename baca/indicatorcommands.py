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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\accent                                                                 %! IC
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
                            -\accent                                                                 %! IC
                            [
                            e''16
                            -\accent                                                                 %! IC
                            ]
                            ef''4
                            -\accent                                                                 %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IC
                            [
                            g''16
                            -\accent                                                                 %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\downbow                                                                %! IC
                            [
                            d'16
                            -\upbow                                                                  %! IC
                            ]
                            bf'4
                            -\downbow                                                                %! IC
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
                            -\downbow                                                                %! IC
                            ]
                            ef''4
                            -\upbow                                                                  %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\downbow                                                                %! IC
                            [
                            g''16
                            -\upbow                                                                  %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\downbow                                                                %! IC
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
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
                            \override TupletBracket.staff-padding = #6                               %! OC1
                            r8
                            c'16
                            -\upbow                                                                  %! IC
                            [
                            d'16
                            -\downbow                                                                %! IC
                            ]
                            bf'4
                            -\upbow                                                                  %! IC
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\downbow                                                                %! IC
                            [
                            e''16
                            -\upbow                                                                  %! IC
                            ]
                            ef''4
                            -\downbow                                                                %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! IC
                            [
                            g''16
                            -\downbow                                                                %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\upbow                                                                  %! IC
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
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
                            \override TupletBracket.staff-padding = #6                               %! OC1
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
                            -\downbow                                                                %! IC
                            [
                            e''16
                            -\upbow                                                                  %! IC
                            ]
                            ef''4
                            -\downbow                                                                %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\upbow                                                                  %! IC
                            [
                            g''16
                            -\downbow                                                                %! IC
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
                            -\arpeggio                                                               %! IC
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
                            -\arpeggio                                                               %! IC
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <g' af''>8
                            -\arpeggio                                                               %! IC
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
                            \override TupletBracket.staff-padding = #7                               %! OC1
                            \clef "alto"                                                             %! IC
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
                            \revert TupletBracket.staff-padding                                      %! OC2
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
                            \override TupletBracket.staff-padding = #7                               %! OC1
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
                            \clef "alto"                                                             %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\baca_staccati #2                                                              %! IC
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
                            -\baca_staccati #2                                                              %! IC
                            [
                            e''16
                            -\baca_staccati #2                                                              %! IC
                            ]
                            ef''4
                            -\baca_staccati #2                                                              %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\baca_staccati #2                                                              %! IC
                            [
                            g''16
                            -\baca_staccati #2                                                              %! IC
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
                            \arpeggioArrowDown                                                       %! IC
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
                            \arpeggioArrowDown                                                       %! IC
                            <ef'' e'' fs'''>8
                            \arpeggio                                                                %! IC
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \arpeggioArrowDown                                                       %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\downbow                                                                %! IC
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
                            -\downbow                                                                %! IC
                            [
                            e''16
                            -\downbow                                                                %! IC
                            ]
                            ef''4
                            -\downbow                                                                %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\downbow                                                                %! IC
                            [
                            g''16
                            -\downbow                                                                %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\espressivo                                                             %! IC
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
                            -\espressivo                                                             %! IC
                            [
                            e''16
                            -\espressivo                                                             %! IC
                            ]
                            ef''4
                            -\espressivo                                                             %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\espressivo                                                             %! IC
                            [
                            g''16
                            -\espressivo                                                             %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            -\fermata                                                                %! IC
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
                            -\fermata                                                                %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\flageolet                                                              %! IC
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
                            -\flageolet                                                              %! IC
                            [
                            e''16
                            -\flageolet                                                              %! IC
                            ]
                            ef''4
                            -\flageolet                                                              %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\flageolet                                                              %! IC
                            [
                            g''16
                            -\flageolet                                                              %! IC
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
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('flageolet')],
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\laissezVibrer                                                          %! IC
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
                            -\laissezVibrer                                                          %! IC
                            [
                            e''16
                            -\laissezVibrer                                                          %! IC
                            ]
                            ef''4
                            ~
                            ef''16
                            -\laissezVibrer                                                          %! IC
                            r16
                            af''16
                            -\laissezVibrer                                                          %! IC
                            [
                            g''16
                            -\laissezVibrer                                                          %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            -\longfermata                                                            %! IC
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
                            -\longfermata                                                            %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\marcato                                                                %! IC
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
                            -\marcato                                                                %! IC
                            [
                            e''16
                            -\marcato                                                                %! IC
                            ]
                            ef''4
                            -\marcato                                                                %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\marcato                                                                %! IC
                            [
                            g''16
                            -\marcato                                                                %! IC
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
                            \set Staff.instrumentName =                                              %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \markup { Fl. }                                                          %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \set Staff.shortInstrumentName =                                         %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \markup { Fl. }                                                          %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                            e'2
                            ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    [MarginMarkup]                                                   %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                            \set Staff.instrumentName =                                              %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \markup { Fl. }                                                          %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \set Staff.shortInstrumentName =                                         %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \markup { Fl. }                                                          %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            f'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            e'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            -\shortfermata                                                           %! IC
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
                            -\shortfermata                                                           %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\staccatissimo                                                          %! IC
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
                            -\staccatissimo                                                          %! IC
                            [
                            e''16
                            -\staccatissimo                                                          %! IC
                            ]
                            ef''4
                            -\staccatissimo                                                          %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\staccatissimo                                                          %! IC
                            [
                            g''16
                            -\staccatissimo                                                          %! IC
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\staccato                                                               %! IC
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
                            -\staccato                                                               %! IC
                            [
                            e''16
                            -\staccato                                                               %! IC
                            ]
                            ef''4
                            -\staccato                                                               %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\staccato                                                               %! IC
                            [
                            g''16
                            -\staccato                                                               %! IC
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                            \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                            \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                            \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                            \clef "percussion"                                                       %! SM8:EXPLICIT_CLEF:IC
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                        %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                            \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                            a4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            b4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            d'4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                            \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                            \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                            \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                            \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                        %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                            \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                            b,4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            e4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                            \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                            \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                            \clef "percussion"                                                       %! SM8:EXPLICIT_CLEF:IC
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                        %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                            \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                            a4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            b4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            d'4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                            \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                            \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                            \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                        %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                            \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                            b,4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            e4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                            \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                            \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                            \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                            \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                        %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                            \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                            g'4.
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            a'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            b'4.
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c''4.
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            :32                                                                      %! IC
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
                            :32                                                                      %! IC
                            [
                            e''16
                            :32                                                                      %! IC
                            ]
                            ef''4
                            :32                                                                      %! IC
                            ~
                            ef''16
                            :32                                                                      %! IC
                            r16
                            af''16
                            :32                                                                      %! IC
                            [
                            g''16
                            :32                                                                      %! IC
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
    return commands.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\stopped                                                                %! IC
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
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('tenuto')],
        selector=selector,
        )

def text_spanner(
    items: typing.Union[str, typing.List],
    *,
    bookend: typing.Union[bool, int] = -1,
    leak: bool = None,
    lilypond_id: int = None,
    piece_selector: typings.Selector = 'baca.group()',
    selector: typings.Selector = 'baca.tleaves()',
    tweaks: typing.List[abjad.LilyPondTweakManager] = None,
    ) -> commands.PiecewiseIndicatorCommand:
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
        ...     baca.text_spanner('pont. => ord.'),
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
        ...     baca.text_spanner('pont. =| ord.'),
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
        ...     baca.text_spanner('pont. -> ord.'),
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
        ...     baca.text_spanner('pont. -| ord.'),
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
        ...     baca.text_spanner('pont. || ord.'),
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
        ...     baca.text_spanner(
        ...         'A || B',
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
        ...     baca.text_spanner(
        ...         'A -> B ->',
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
        ...     baca.text_spanner(
        ...         'A || B',
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
        ...     baca.text_spanner(
        ...         'A -> B ->',
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
        ...     baca.text_spanner(
        ...         'A -| B -|',
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
        '||': 'invisible_line',
        '->': 'solid_line_with_arrow',
        '-|': 'solid_line_with_hook',
        }
    if isinstance(items, str):
        items_ = []
        current_item: typing.List[str] = []
        for word in items.split():
            if word in shape_to_style:
                if current_item:
                    item_ = ' '.join(current_item)
                    items_.append(item_)
                    current_item = []
                items_.append(word)
            else:
                current_item.append(word)
        if current_item:
            item_ = ' '.join(current_item)
            items_.append(item_)
        items = items_
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
    cyclic_items = abjad.CyclicTuple(items)
    for i, item in enumerate(cyclic_items):
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
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: typing.Union[abjad.LilyPondLiteral, abjad.Markup]
        if isinstance(right_text, str):
            if 'hook' not in style:
                string = rf'\markup \baca-right "{right_text}"'
                right_markup = abjad.LilyPondLiteral(string)
            else:
                right_markup = abjad.Markup.from_literal(right_text)
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
            scoping.Command._apply_tweaks(start_text_span, tweaks)
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
        # TODO: find some way to make these tweaks explicit to composer
        manager = abjad.tweak(bookended_spanner_start)
        manager.bound_details__right__stencil_align_dir_y = abjad.Center
        if 'hook' in style:
            manager.bound_details__right__padding = 1.25
        else:
            manager.bound_details__right__padding = 0.5
        bundle = commands.IndicatorBundle(
            stop_text_span,
            start_text_span,
            bookended_spanner_start=bookended_spanner_start,
            enchained=True,
            )
        bundles.append(bundle)
    return commands.PiecewiseIndicatorCommand(
        bookend=bookend,
        bundles=bundles,
        leak=leak,
        piece_selector=piece_selector,
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
    return commands.IndicatorCommand(
        indicators=[abjad.Articulation('verylongfermata')],
        selector=selector,
        )
