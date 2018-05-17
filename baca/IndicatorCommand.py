import abjad
import baca
import collections
import typing
from .Command import Command
from .SegmentMaker import SegmentMaker
from .Typing import Selector


class IndicatorCommand(Command):
    r"""
    Indicator command.

    >>> from abjad import rhythmos as rhythmos

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rhythmos.Talea(
        ...                 counts=[5, 4, 4, 5, 4, 4, 4],
        ...                 denominator=32,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
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
                            c'8
                            \fermata                                                                 %! IC
                            ~
                            [
                            c'32
                            d'8
                            \fermata                                                                 %! IC
                            bf'8
                            \fermata                                                                 %! IC
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            \fermata                                                                 %! IC
                            ~
                            [
                            fs''32
                            e''8
                            \fermata                                                                 %! IC
                            ef''8
                            \fermata                                                                 %! IC
                            af''8
                            \fermata                                                                 %! IC
                            ~
                            af''32
                            g''8
                            \fermata                                                                 %! IC
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            \fermata                                                                 %! IC
                            ~
                            [
                            a'32
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
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
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
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
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                e'8
                                \fermata                                                             %! IC
                                [
            <BLANKLINE>
                                d''8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                f'8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                e''8
                                \fermata                                                             %! IC
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                g'8
                                \fermata                                                             %! IC
                                [
            <BLANKLINE>
                                f''8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                e'8
                                \fermata                                                             %! IC
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                d''8
                                \fermata                                                             %! IC
                                [
            <BLANKLINE>
                                f'8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                e''8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                g'8
                                \fermata                                                             %! IC
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                f''8
                                \fermata                                                             %! IC
                                [
            <BLANKLINE>
                                e'8
                                \fermata                                                             %! IC
            <BLANKLINE>
                                d''8
                                \fermata                                                             %! IC
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_indicators',
        '_redundant',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        context: str = None,
        deactivate: bool = None,
        indicators: typing.List[typing.Any] = None,
        redundant: bool = None,
        selector: Selector = 'baca.pheads()',
        tags: typing.List[abjad.Tag] = None,
        tweaks: typing.List[typing.Tuple] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        indicators_ = None
        if indicators is not None:
            if isinstance(indicators, collections.Iterable):
                indicators_ = abjad.CyclicTuple(indicators)
            else:
                indicators_ = abjad.CyclicTuple([indicators])
        self._indicators = indicators_
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        if tweaks is not None:
            assert isinstance(tweaks, list), repr(tweaks)
            assert all(isinstance(_, tuple) for _ in tweaks), repr(tweaks)
        self._tweaks = tweaks
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.indicators is None:
            return
        if self.redundant is True:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, leaf in enumerate(baca.select(argument).leaves()):
            indicators = self.indicators[i]
            indicators = self._token_to_indicators(indicators)
            for indicator in indicators:
                self._apply_tweaks(indicator)
                reapplied = self._remove_reapplied_wrappers(leaf, indicator)
                wrapper = abjad.attach(
                    indicator,
                    leaf,
                    context=self.context,
                    deactivate=self.deactivate,
                    tag=self.tag.prepend('IC'),
                    wrapper=True,
                    )
                if indicator == reapplied:
                    if (isinstance(indicator, abjad.Dynamic) and
                        indicator.sforzando):
                        status = 'explicit'
                    else:
                        status = 'redundant'
                    SegmentMaker._treat_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        status,
                        )

    ### PRIVATE METHODS ###

    @staticmethod
    def _token_to_indicators(token):
        result = []
        if not isinstance(token, (tuple, list)):
            token = [token]
        for item in token:
            if item is None:
                continue
            result.append(item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context name.
        """
        return self._context

    @property
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        r"""
        Gets indicators.

        ..  container:: example

            Attaches fermata to head of every pitched logical tie:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
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
                                c'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                c'32
                                d'8
                                \fermata                                                                 %! IC
                                bf'8
                                \fermata                                                                 %! IC
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IC
                                ~
                                [
                                fs''32
                                e''8
                                \fermata                                                                 %! IC
                                ef''8
                                \fermata                                                                 %! IC
                                af''8
                                \fermata                                                                 %! IC
                                ~
                                af''32
                                g''8
                                \fermata                                                                 %! IC
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns fermatas:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(
            ...         indicators=[
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None,
            ...             ],
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
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
                                c'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                c'32
                                d'8
                                bf'8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IC
                                ~
                                [
                                fs''32
                                e''8
                                ef''8
                                af''8
                                \fermata                                                                 %! IC
                                ~
                                af''32
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

        """
        return self._indicators

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant

    @property
    def tweaks(self) -> typing.Optional[typing.List[typing.Tuple]]:
        """
        Gets tweaks.
        """
        return self._tweaks
