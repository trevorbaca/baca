import abjad
import baca
from .Command import Command


class ClusterCommand(Command):
    r"""Cluster command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(baca.clusters([3, 4]))

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
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <c' e' g'>16 [
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <d' f' a' c''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <bf' d'' f''>16 ]
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <fs'' a'' c''' e'''>16 [
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e'' g'' b''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <ef'' g'' b'' d'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <af'' c''' e'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <g'' b'' d''' f'''>16 ]
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <a' c'' e''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                    }
                }
            >>

    ..  container:: example

        In tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.clusters(
        ...         [3, 4],
        ...         selector=baca.tuplets()[1:2].plts().group(),
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
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <fs'' a'' c'''>16 [
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e'' g'' b'' d'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <ef'' g'' b''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <af'' c''' e''' g'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <g'' b'' d'''>16 ]
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                        {
                            a'16
                        }
                    }
                }
            >>

    ..  container:: example

        PLT -1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.clusters([3, 4], selector=baca.plt(-1)),
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
                            fs''16 [
                            e''16
                            ef''16
                            af''16
                            g''16 ]
                        }
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <a' c'' e''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
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
        ...     baca.clusters([3, 4], start_pitch='E4'),
        ...     baca.make_notes(repeat_ties=True),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "Global Context" <<
                    \context GlobalSkips = "Global Skips" {
            <BLANKLINE>
                        %%% Global Skips [measure 1] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% Global Skips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% Global Skips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% Global Skips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
            <BLANKLINE>
                            %%% MusicVoice [measure 1] %%%
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            \clef "treble"
                            <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
            <BLANKLINE>
                            %%% MusicVoice [measure 2] %%%
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
            <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
            <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \bar "|"
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_hide_flat_markup',
        '_start_pitch',
        '_widths',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        hide_flat_markup=None,
        selector='baca.plts()',
        start_pitch=None,
        widths=None,
        ):
        Command.__init__(self, selector=selector)
        assert isinstance(hide_flat_markup, (bool, type(None)))
        self._hide_flat_markup = hide_flat_markup
        if start_pitch is not None:
            start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch = start_pitch
        assert abjad.mathtools.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = baca.select(argument).leaf(0)
        root = abjad.inspect(leaf).get_parentage().root
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(baca.select(argument).plts()):
                width = self.widths[i]
                self._make_cluster(plt, width)

    ### PRIVATE METHODS ###

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        indicator = abjad.KeyCluster(
            include_black_keys=not self.hide_flat_markup,
            )
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            abjad.mutate(pleaf).replace(chord)
            abjad.attach(indicator, chord)
            abjad.attach('repeat pitch allowed', chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval('M3')
            pitch = abjad.NamedPitch(pitch._get_diatonic_pitch_name())
            assert pitch.accidental.name == 'natural'
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def hide_flat_markup(self):
        r'''Is true when cluster hides flat markup.

        ..  container:: example

            Hides flat markup:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.pitches('E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.natural_clusters(widths=[3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \clef "treble"
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_flat_markup

    @property
    def selector(self):
        r'''Selects PLTs.

        ..  container:: example

            >>> baca.clusters([3, 4]).selector
            baca.plts()

        Returns selector.
        '''
        return self._selector

    @property
    def start_pitch(self):
        r'''Gets start pitch.

        ..  container:: example

            Takes start pitch from input notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('C4 D4 E4 F4'),
            ...     baca.clusters([3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \clef "treble"
                                <c' e' g'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <d' f' a'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <f' a' c''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Sets start pitch explicitly:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.clusters([3], start_pitch='G4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \clef "treble"
                                <g' b' d''>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Set to named pitch or none.

        Returns named pitch or none.
        '''
        return self._start_pitch

    @property
    def widths(self):
        r'''Gets widths.

        ..  container:: example

            Increasing widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clusters([1, 2, 3, 4], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \clef "treble"
                                <e'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b' d''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Patterned widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clusters([1, 3], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \clef "treble"
                                <e'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Leaves notes and chords unchanged:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('E4', repeats=True),
            ...     baca.clusters([]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "Global Context" <<
                        \context GlobalSkips = "Global Skips" {
                <BLANKLINE>
                            %%% Global Skips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% Global Skips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% Global Skips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble"
                                e'2
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'4.
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'2
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'4.
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

        Set to nonnegative integers or none.

        Returns nonnegative integers or none.
        '''
        return self._widths
