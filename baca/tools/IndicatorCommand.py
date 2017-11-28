import abjad
import baca
import collections
from .Command import Command


class IndicatorCommand(Command):
    r'''Attach command.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.IndicatorCommand([abjad.Fermata()]),
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'8 \fermata ~ [
                            c'32
                            d'8 \fermata
                            bf'8 \fermata ]
                        }
                        {
                            fs''8 \fermata ~ [
                            fs''32
                            e''8 \fermata
                            ef''8 \fermata
                            af''8 \fermata ~
                            af''32
                            g''8 \fermata ]
                        }
                        {
                            a'8 \fermata ~ [
                            a'32 ]
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
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.IndicatorCommand([abjad.Fermata()]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY-BAR:1
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR:2
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR:1
                                e'8 \fermata [
            <BLANKLINE>
                                d''8 \fermata
            <BLANKLINE>
                                f'8 \fermata
            <BLANKLINE>
                                e''8 \fermata ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                g'8 \fermata [
            <BLANKLINE>
                                f''8 \fermata
            <BLANKLINE>
                                e'8 \fermata ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                d''8 \fermata [
            <BLANKLINE>
                                f'8 \fermata
            <BLANKLINE>
                                e''8 \fermata
            <BLANKLINE>
                                g'8 \fermata ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                f''8 \fermata [
            <BLANKLINE>
                                e'8 \fermata
            <BLANKLINE>
                                d''8 \fermata ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indicators',
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(self, indicators=None, selector='baca.pheads()', tag=None):
        Command.__init__(self, selector=selector)
        if indicators is not None:
            if isinstance(indicators, collections.Iterable):
                indicators = abjad.CyclicTuple(indicators)
            else:
                indicators = abjad.CyclicTuple([indicators])
        self._indicators = indicators
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.indicators is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, leaf in enumerate(baca.select(argument).leaves()):
            indicators = self.indicators[i]
            indicators = self._token_to_indicators(indicators)
            for indicator in indicators:
                abjad.attach(indicator, leaf, tag=self.tag)

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
    def indicators(self):
        r'''Gets indicators.

        ..  container:: example

            Attaches fermata to head of every pitched logical tie:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand([abjad.Fermata()]),
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'8 \fermata ~ [
                                c'32
                                d'8 \fermata
                                bf'8 \fermata ]
                            }
                            {
                                fs''8 \fermata ~ [
                                fs''32
                                e''8 \fermata
                                ef''8 \fermata
                                af''8 \fermata ~
                                af''32
                                g''8 \fermata ]
                            }
                            {
                                a'8 \fermata ~ [
                                a'32 ]
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'8 \fermata ~ [
                                c'32
                                d'8
                                bf'8 ]
                            }
                            {
                                fs''8 \fermata ~ [
                                fs''32
                                e''8
                                ef''8
                                af''8 \fermata ~
                                af''32
                                g''8 ]
                            }
                            {
                                a'8 \fermata ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to indicators or none.

        Returns indicators or none.
        '''
        return self._indicators

    @property
    def tag(self):
        r'''Gets tag.

        Returns string or none.
        '''
        return self._tag
