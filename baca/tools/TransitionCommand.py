import abjad
import baca
import copy
from .Command import Command


class TransitionCommand(Command):
    r'''Transition command.

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.TransitionCommand(
            ...         start_markup=baca.markup.ord_(),
            ...         stop_markup=baca.markup.pont(),
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     talea_denominator=4,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_runs(),
            ...     baca.TransitionCommand(
            ...         start_markup=baca.markup.ord_(),
            ...         stop_markup=baca.markup.pont(),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, collection_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_selector',
        '_solid',
        '_start_markup',
        '_stop_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector=None,
        solid=None,
        start_markup=None,
        stop_markup=None,
        ):
        assert start_markup is not None or stop_markup is not None
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector
        if solid is not None:
            solid = bool(solid)
        self._solid = solid
        self._start_markup = start_markup
        self._stop_markup = stop_markup

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = abjad.select(argument).by_leaf()
        spanner = abjad.TextSpanner()
        abjad.attach(spanner, leaves)
        start_leaf = leaves[0]
        stop_leaf = leaves[-1]
        start_markup = self.start_markup
        if isinstance(start_markup, baca.AttachCommand):
            start_markup = start_markup.arguments[0]
        if start_markup is not None:
            assert isinstance(start_markup, abjad.Markup), repr(start_markup)
            start_markup = copy.copy(start_markup)
            start_markup = start_markup.override(('font-name', 'Palatino'))
            spanner.attach(start_markup, start_leaf)
        arrow = self._get_arrow()
        spanner.attach(arrow, start_leaf)
        stop_markup = self.stop_markup
        if isinstance(stop_markup, baca.AttachCommand):
            stop_markup = stop_markup.arguments[0]
        if stop_markup is not None:
            assert isinstance(stop_markup, abjad.Markup), repr(stop_markup)
            stop_markup = copy.copy(stop_markup)
            stop_markup = stop_markup.override(('font-name', 'Palatino'))
            spanner.attach(stop_markup, stop_leaf)

    ### PRIVATE METHODS ###

    def _get_arrow(self):
        if self.solid:
            return abjad.ArrowLineSegment()
        return self._make_dashed_arrow()

    @staticmethod
    def _make_dashed_arrow():
        return abjad.ArrowLineSegment(
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
    def selector(self):
        r'''Gets selector.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def solid(self):
        r'''Is true when command renders transition as a solid line instead
        of a dashed line.

        Is false when command renders transitions as a dashed line.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._solid

    @property
    def start_markup(self):
        r'''Gets command start markup.

        Set to markup.

        Returns markup.
        '''
        return self._start_markup

    @property
    def stop_markup(self):
        r'''Gets command stop markup.

        Set to markup.

        Returns markup.
        '''
        return self._stop_markup
