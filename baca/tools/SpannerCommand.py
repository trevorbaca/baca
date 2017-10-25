import abjad
import baca
from .Command import Command


class SpannerCommand(Command):
    r'''Spanner command.

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.SpannerCommand(
            ...         selector=baca.select().tuplets(),
            ...         spanner=abjad.Slur(),
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

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

        With collection-maker:

        ..  note:: Teach SegmentMaker about SpannerCommand.

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.SpannerCommand(
            ...         selector=baca.select().tuplets(),
            ...         spanner=abjad.Slur(),
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
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

            >>> baca.SpannerCommand()
            SpannerCommand(selector=baca.select().leaves().group())

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotation',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector='baca.select().leaves().group()',
        spanner=None,
        ):
        Command.__init__(self, selector=selector)
        if spanner is not None:
            assert isinstance(spanner, abjad.Spanner)
        self._spanner = spanner
        self._annotation = None

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
#        if argument is None:
#            return
#        if self.selector is not None:
#            argument = self.selector(argument)
#        selections = self._to_selection_list(argument)
#        if self.target is not None:
#            selections = [self.target(_) for _ in selections]
#        selections = self._to_selection_list(selections)
        selections = self._select(music)
        if False:
            print(format(self.selector))
            print()
            print(argument)
            print()
            print(selections)
            print()
        if self.spanner is None:
            return
        for selection in selections:
            spanner = abjad.new(self.spanner)
            leaves = abjad.select(selection).by_leaf()
            if len(leaves) <= 1:
                continue
            if isinstance(spanner, abjad.Tie):
                for leaf in leaves:
                    abjad.detach(abjad.Tie, leaf)
            abjad.attach(spanner, leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects wrapped leaves:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.SpannerCommand(spanner=abjad.Slur()),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

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

                >>> music_maker = baca.MusicMaker(
                ...     baca.SpannerCommand(spanner=abjad.Slur()),
                ...     )

            ::

                >>> collections = [[1]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

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

                >>> music_maker = baca.MusicMaker()

            ::

                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[14, 14, 14]],
                ...     counts=[5],
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

                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[14, 14, 14]],
                ...     baca.SpannerCommand(spanner=abjad.Tie()),
                ...     counts=[5],
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

        Set to spanner or none.

        Returns spanner or none.
        '''
        return self._spanner
