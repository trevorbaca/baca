# -*- coding: utf-8 -*-
import abjad
import baca


class ArticulationSpecifier(abjad.abctools.AbjadObject):
    r'''Articulation specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With music-maker:

        Selects heads of pitched logical ties by default:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['>'],
            ...         ),
            ...     baca.tools.MusicRhythmSpecifier(
            ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                            c'8 -\accent ~ [
                            c'32
                            d'8 -\accent
                            bf'8 -\accent ]
                        }
                        {
                            fs''8 -\accent ~ [
                            fs''32
                            e''8 -\accent
                            ef''8 -\accent
                            af''8 -\accent ~
                            af''32
                            g''8 -\accent ]
                        }
                        {
                            a'8 -\accent ~ [
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
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['.'],
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
                                e'8 -\staccato [
                                d''8 -\staccato
                                f'8 -\staccato
                                e''8 -\staccato ]
                            }
                            {
                                g'8 -\staccato [
                                f''8 -\staccato
                                e'8 -\staccato ]
                            }
                            {
                                d''8 -\staccato [
                                f'8 -\staccato
                                e''8 -\staccato
                                g'8 -\staccato ]
                            }
                            {
                                f''8 -\staccato [
                                e'8 -\staccato
                                d''8 -\staccato ]
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
        '_articulations',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        articulations=None,
        selector=None,
        ):
        if articulations is not None:
            prototype = (abjad.Articulation, str, tuple, list, type(None))
            assert all(isinstance(_, prototype) for _ in articulations)
        self._articulations = articulations
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
        if not self.articulations:
            return
        articulations = abjad.CyclicTuple(self.articulations)
        selector = self.selector or baca.select_plt_heads()
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            leaves = abjad.select(selection).by_leaf()
            for i, leaf in enumerate(leaves):
                assert isinstance(leaf, abjad.Leaf), repr(leaf)
                articulations_ = articulations[i]
                articulations_ = self._token_to_articulations(articulations_)
                for articulation_ in articulations_:
                    abjad.attach(articulation_, leaf)

    ### PRIVATE METHODS ###

    @staticmethod
    def _token_to_articulations(token):
        result = []
        if not isinstance(token, (tuple, list)):
            token = [token]
        for item in token:
            if item is None:
                continue
            articulation = abjad.Articulation(item)
            result.append(articulation)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def articulations(self):
        r'''Gets articulations.

        ..  container:: example

            Accents the head of every pitched logical tie:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\accent ~ [
                                c'32
                                d'8 -\accent
                                bf'8 -\accent ]
                            }
                            {
                                fs''8 -\accent ~ [
                                fs''32
                                e''8 -\accent
                                ef''8 -\accent
                                af''8 -\accent ~
                                af''32
                                g''8 -\accent ]
                            }
                            {
                                a'8 -\accent ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns accents:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=[
                ...             '>', None, None,
                ...             '>', None, None,
                ...             '>', None,
                ...             ],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\accent ~ [
                                c'32
                                d'8
                                bf'8 ]
                            }
                            {
                                fs''8 -\accent ~ [
                                fs''32
                                e''8
                                ef''8
                                af''8 -\accent ~
                                af''32
                                g''8 ]
                            }
                            {
                                a'8 -\accent ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns accents with staccati:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=[
                ...             '>', '.', '.',
                ...             '>', '.', '.',
                ...             '>', '.',
                ...             ],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\accent ~ [
                                c'32
                                d'8 -\staccato
                                bf'8 -\staccato ]
                            }
                            {
                                fs''8 -\accent ~ [
                                fs''32
                                e''8 -\staccato
                                ef''8 -\staccato
                                af''8 -\accent ~
                                af''32
                                g''8 -\staccato ]
                            }
                            {
                                a'8 -\accent ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns accented tenuti with staccati:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=[
                ...             ('>', '-'), '.', '.',
                ...             ('>', '-'), '.', '.',
                ...             ('>', '-'), '.',
                ...             ],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\accent -\tenuto ~ [
                                c'32
                                d'8 -\staccato
                                bf'8 -\staccato ]
                            }
                            {
                                fs''8 -\accent -\tenuto ~ [
                                fs''32
                                e''8 -\staccato
                                ef''8 -\staccato
                                af''8 -\accent -\tenuto ~
                                af''32
                                g''8 -\staccato ]
                            }
                            {
                                a'8 -\accent -\tenuto ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            With reiterated dynamics:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['f'],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\f ~ [
                                c'32
                                d'8 -\f
                                bf'8 -\f ]
                            }
                            {
                                fs''8 -\f ~ [
                                fs''32
                                e''8 -\f
                                ef''8 -\f
                                af''8 -\f ~
                                af''32
                                g''8 -\f ]
                            }
                            {
                                a'8 -\f ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to articulation tokens or none.

        Returns articulation tokens or none.
        '''
        return self._articulations

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects heads of pitched logical ties by default:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
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
                                c'8 -\accent ~ [
                                c'32
                                d'8 -\accent
                                bf'8 -\accent ]
                            }
                            {
                                fs''8 -\accent ~ [
                                fs''32
                                e''8 -\accent
                                ef''8 -\accent
                                af''8 -\accent ~
                                af''32
                                g''8 -\accent ]
                            }
                            {
                                a'8 -\accent ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
