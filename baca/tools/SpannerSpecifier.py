# -*- coding: utf-8 -*-
import abjad


class SpannerSpecifier(abjad.abctools.AbjadObject):
    r'''Spanner specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.SpannerSpecifier(
            ...         selector=baca.select.every_tuplet(),
            ...         spanner=abjad.Slur(),
            ...         ),
            ...     )

        ::

            >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker('Voice 1', segments)
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16 [ (
                            d'16
                            bf'16 ] )
                        }
                        {
                            fs''16 [ (
                            e''16
                            ef''16
                            af''16
                            g''16 ] )
                        }
                        {
                            a'16
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        ..  note:: Teach SegmentMaker about SpannerSpecifier.

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     baca.make_even_run_rhythm_specifier(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.tools.SpannerSpecifier(
            ...         selector=baca.select.every_tuplet(),
            ...         spanner=abjad.Slur(),
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
                                e'8 [
                                d''8
                                f'8
                                e''8 ]
                            }
                            {
                                g'8 [
                                f''8
                                e'8 ]
                            }
                            {
                                d''8 [
                                f'8
                                e''8
                                g'8 ]
                            }
                            {
                                f''8 [
                                e'8
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        ::

            >>> baca.tools.SpannerSpecifier()
            SpannerSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_selector',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector=None,
        spanner=None,
        ):
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector
        if spanner is not None:
            assert isinstance(spanner, abjad.spannertools.Spanner)
        self._spanner = spanner

    ### SPECIAL METHODS ###

    def __call__(self, selection):
        r'''Calls spanner figure specifier on `selection`.

        Returns none.
        '''
        if self.spanner is None:
            return
        selector = self._get_selector()
        #print(selector)
        #print(selection)
        selections = selector(selection)
        #print(selections)
        for index, selection in enumerate(selections):
            self._apply_payload(index, selection)
            
    ### PRIVATE METHODS ###

    def _apply_payload(self, index, selection):
        spanner = abjad.new(self.spanner)
        leaves = list(abjad.iterate(selection).by_leaf())
        if 1 < len(leaves):
            if isinstance(spanner, abjad.Tie):
                for leaf in leaves:
                    abjad.detach(abjad.Tie, leaf)
            abjad.attach(spanner, leaves)

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.select()
            selector = selector.by_leaf()
            return selector
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects leaves by default:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=abjad.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16 )
                            }
                        }
                    }
                >>

        ..  container:: example

            Spanner refuses to span a single leaf:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=abjad.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [[1]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                cs'16
                            }
                        }
                    }
                >>

        Defaults to leaves.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def spanner(self):
        r'''Gets spanner.

        ..  container:: example

            Ties are smart enough to remove existing ties prior to attach:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[14, 14, 14]],
                ...     talea_counts=[5],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                d''4 ~
                                d''16
                                d''4 ~
                                d''16
                                d''4 ~
                                d''16
                            }
                        }
                    }
                >>

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[14, 14, 14]],
                ...     baca.tools.SpannerSpecifier(spanner=abjad.Tie()),
                ...     talea_counts=[5],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                d''4 ~
                                d''16 ~
                                d''4 ~
                                d''16 ~
                                d''4 ~
                                d''16
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to spanner or none.

        Returns spanner or none.
        '''
        return self._spanner
