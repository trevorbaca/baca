# -*- coding: utf-8 -*-
import abjad
import copy


class TransitionSpecifier(abjad.abctools.AbjadObject):
    r'''Transition specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With figure-maker:

        ::

            >>> figure_maker = baca.FigureMaker(
            ...     baca.tools.TransitionSpecifier(
            ...         start_markup=baca.markup.ord_(),
            ...         stop_markup=baca.markup.pont(),
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     collections,
            ...     talea_denominator=4,
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
                            \once \override TextSpanner.arrow-width = 0.25
                            \once \override TextSpanner.bound-details.left-broken.text = ##f
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                            \once \override TextSpanner.bound-details.left.text = \markup {
                                \concat
                                    {
                                        \override
                                            #'(font-name . "Palatino")
                                            \whiteout
                                                \upright
                                                    ord.
                                        \hspace
                                            #0.5
                                    }
                                }
                            \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                            \once \override TextSpanner.bound-details.right-broken.padding = 0
                            \once \override TextSpanner.bound-details.right.arrow = ##t
                            \once \override TextSpanner.bound-details.right.padding = 1.75
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                            \once \override TextSpanner.dash-fraction = 0.25
                            \once \override TextSpanner.dash-period = 1.5
                            c'4 \startTextSpan
                            d'4
                            bf'4
                        }
                        {
                            fs''4
                            e''4
                            ef''4
                            af''4
                            g''4
                        }
                        {
                            a'4 \stopTextSpan ^ \markup {
                                \override
                                    #'(font-name . "Palatino")
                                    \whiteout
                                        \upright
                                            pont.
                                }
                        }
                    }
                }
            >>

    ..  container:: example

        With collection-maker:

        ::

            >>> collection_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = collection_maker.append_specifiers(
            ...     ('vn', baca.select_stages(1)),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_run_rhythm_specifier(),
            ...     baca.tools.TransitionSpecifier(
            ...         start_markup=baca.markup.ord_(),
            ...         stop_markup=baca.markup.pont(),
            ...         ),
            ...     )

        ::

            >>> result = collection_maker(is_doc_example=True)
            >>> lilypond_file, collection_metadata = result
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
                                            \override
                                                #'(font-name . "Palatino")
                                                \whiteout
                                                    \upright
                                                        ord.
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                                \once \override TextSpanner.bound-details.right-broken.padding = 0
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 1.75
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                e'8 [ \startTextSpan
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8 ]
                            }
                            {
                                f'8 [
                                e'8
                                f'8
                                e'8 ]
                            }
                            {
                                f'8 [
                                e'8
                                f'8 ] \stopTextSpan ^ \markup {
                                    \override
                                        #'(font-name . "Palatino")
                                        \whiteout
                                            \upright
                                                pont.
                                    }
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
        '_solid',
        '_start_markup',
        '_stop_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        solid=None,
        start_markup=None,
        stop_markup=None,
        ):
        assert start_markup is not None or stop_markup is not None
        if solid is not None:
            solid = bool(solid)
        self._solid = solid
        self._start_markup = start_markup
        self._stop_markup = stop_markup

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        leaves = abjad.select(argument).by_leaf()
        start_leaf = leaves[0]
        stop_leaf = leaves[-1]
        if self.start_markup is not None:
            start_markup = copy.copy(self.start_markup)
            start_markup = start_markup.override(('font-name', 'Palatino'))
            abjad.attach(start_markup, start_leaf, is_annotation=True)
        arrow = self._get_arrow()
        abjad.attach(arrow, start_leaf)
        if self.stop_markup is not None:
            stop_markup = copy.copy(self.stop_markup)
            stop_markup = stop_markup.override(('font-name', 'Palatino'))
            abjad.attach(stop_markup, stop_leaf, is_annotation=True)
        abjad.attach(abjad.TextSpanner(), leaves)

    ### PRIVATE METHODS ###

    def _get_arrow(self):
        if self.solid:
            return abjad.Arrow()
        return self._make_dashed_arrow()

    @staticmethod
    def _make_dashed_arrow():
        return abjad.Arrow(
            dash_fraction=0.25,
            dash_period=1.5,
            left_broken_text=False,
            left_hspace=0.5,
            right_broken_arrow=False,
            right_broken_padding=0,
            right_padding=1.75,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def solid(self):
        r'''Is true when specifier renders transition as a solid line instead
        of a dashed line.

        Is false when specifier renders transitions as a dashed line.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._solid

    @property
    def start_markup(self):
        r'''Gets start markup of transition specifier.

        Set to markup.

        Returns markup.
        '''
        return self._start_markup

    @property
    def stop_markup(self):
        r'''Gets stop markup of transition specifier.

        Set to markup.

        Returns markup.
        '''
        return self._stop_markup
