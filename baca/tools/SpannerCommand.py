import abjad
import baca
from .Command import Command


class SpannerCommand(Command):
    r'''Spanner command.

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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16 [
                            d'16
                            bf'16 ]
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

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.SpannerCommand(
        ...         selector=baca.leaves()[4:7],
        ...         spanner=abjad.Slur(),
        ...         ),
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
                        \bar "" % SEGMENT:EMPTY_BAR:1
                        s1 * 1/2
                            - \markup { % STAGE_NUMBER:2
                                \fontsize % STAGE_NUMBER:2
                                    #-3 % STAGE_NUMBER:2
                                    \with-color % STAGE_NUMBER:2
                                        #(x11-color 'DarkCyan) % STAGE_NUMBER:2
                                        [1] % STAGE_NUMBER:2
                                } % STAGE_NUMBER:2
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
                                \clef "treble" % SEGMENT:EXPLICIT-CLEF:2
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CLEF:COLOR:1
                                e'8 [
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                g'8 [ (
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                e'8 ] )
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                d''8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                g'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                f''8 [
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                d''8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> baca.SpannerCommand()
        SpannerCommand(selector=baca.tleaves())

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotation',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(self, selector='baca.tleaves()', spanner=None):
        Command.__init__(self, selector=selector)
        if spanner is not None:
            assert isinstance(spanner, abjad.Spanner)
        self._spanner = spanner
        self._annotation = None

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns spanner (for handoff to piecewise command).
        '''
        if argument is None:
            return
        if self.spanner is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = abjad.select(argument).leaves()
        spanner = abjad.new(self.spanner)
        abjad.attach(spanner, leaves)
        return spanner

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects trimmed leaves by default:

            >>> music_maker = baca.MusicMaker(baca.slur())

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

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def spanner(self):
        r'''Gets spanner.

        ..  container:: example

            Ties are smart enough to remove existing ties prior to attach:

            >>> music_maker = baca.MusicMaker()

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     counts=[5],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     baca.SpannerCommand(spanner=abjad.Tie()),
            ...     counts=[5],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
