import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class SpannerCommand(Command):
    r"""
    Spanner command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.SpannerCommand(
        ...         selector=baca.tuplet(1),
        ...         spanner=abjad.Slur(),
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
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            (                                                                        %! SC
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                            )                                                                        %! SC
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
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
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.SpannerCommand(
        ...         selector=baca.leaves()[4:7],
        ...         spanner=abjad.Slur(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
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
                            (                                                                        %! SC
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
                            )                                                                        %! SC
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
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> baca.SpannerCommand()
        SpannerCommand(selector=baca.leaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_broken',
        '_right_broken',
        '_spanner',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        left_broken: bool = None,
        right_broken: bool = None,
        selector: Selector = 'baca.leaves()',
        spanner: abjad.Spanner = None,
        tags: typing.List[abjad.Tag] = None,
        tweaks: typing.List[typing.Tuple] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        self._spanner = spanner
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags
        if tweaks is not None:
            assert isinstance(tweaks, list), repr(tweaks)
            assert all(isinstance(_, tuple) for _ in tweaks), repr(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on ``argument``.

        Returns spanner (for handoff to piecewise command).
        """
        if argument is None:
            return
        if self.spanner is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = abjad.select(argument).leaves()
        spanner = abjad.new(self.spanner)
        self._apply_tweaks(spanner)
        abjad.attach(
            spanner,
            leaves,
            deactivate=self.deactivate,
            left_broken=self.left_broken,
            right_broken=self.right_broken,
            tag=self.tag.prepend('SC'),
            )
        return spanner

    ### PUBLIC PROPERTIES ###

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-broken.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-broken.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.

        ..  container:: example

            Selects trimmed leaves by default:

            >>> music_maker = baca.MusicMaker(baca.slur())

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
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                )                                                                        %! SC
                            }
                        }
                    }
                >>

        Set to selector or none.

        Returns selector or none.
        """
        return self._selector

    @property
    def spanner(self) -> typing.Optional[abjad.Spanner]:
        r"""
        Gets spanner.

        ..  container:: example

            Ties are smart enough to remove existing ties prior to attach:

            >>> music_maker = baca.MusicMaker()

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     counts=[5],
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
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     baca.SpannerCommand(spanner=abjad.Tie()),
            ...     counts=[5],
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
                                d''4
                                ~                                                                        %! SC
                                d''16
                                ~                                                                        %! SC
                                d''4
                                ~                                                                        %! SC
                                d''16
                                ~                                                                        %! SC
                                d''4
                                ~                                                                        %! SC
                                d''16
                            }
                        }
                    }
                >>

        Set to spanner or none.

        Returns spanner or none.
        """
        return self._spanner

    @property
    def tweaks(self) -> typing.Optional[typing.List[typing.Tuple]]:
        """
        Gets tweaks.
        """
        return self._tweaks
