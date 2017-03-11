# -*- coding: utf-8 -*-
import abjad
import baca


class IndicatorSpecifier(abjad.abctools.AbjadObject):
    r'''Indicator specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.tools.IndicatorSpecifier(
            ...         indicators=[abjad.Fermata()],
            ...         ),
            ...     baca.tools.FigureRhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
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

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select_stages(1)),
            ...     baca.even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.tools.IndicatorSpecifier(
            ...         indicators=[abjad.Fermata()],
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'8 \fermata [
                                d''8 \fermata
                                f'8 \fermata
                                e''8 \fermata ]
                            }
                            {
                                g'8 \fermata [
                                f''8 \fermata
                                e'8 \fermata ]
                            }
                            {
                                d''8 \fermata [
                                f'8 \fermata
                                e''8 \fermata
                                g'8 \fermata ]
                            }
                            {
                                f''8 \fermata [
                                e'8 \fermata
                                d''8 \fermata ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_indicators',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indicators=None,
        selector=None,
        ):
        self._indicators = indicators
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if not argument:
            return
        if self.indicators is None:
            return
        indicators = abjad.CyclicTuple(self.indicators)
        selector = self.selector or baca.select_pitched_heads()
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            leaves = abjad.select(selection).by_leaf()
            for i, leaf in enumerate(leaves):
                indicators_ = indicators[i]
                indicators_ = self._token_to_indicators(indicators_)
                for indicator_ in indicators_:
                    abjad.attach(indicator_, leaf)

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

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.IndicatorSpecifier(
                ...         indicators=[abjad.Fermata()],
                ...         ),
                ...     baca.tools.FigureRhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
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

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.IndicatorSpecifier(
                ...         indicators=[
                ...             abjad.Fermata(), None, None,
                ...             abjad.Fermata(), None, None,
                ...             abjad.Fermata(), None,
                ...             ],
                ...         ),
                ...     baca.tools.FigureRhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
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
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
