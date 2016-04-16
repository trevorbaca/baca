# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import mutate


class ClusterSpecifier(abctools.AbjadObject):
    r'''Cluster specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.**

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4'),
            ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
            ...         baca.tools.ClusterSpecifier(
            ...             widths=[3, 4],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
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
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_hide_flat_markup',
        '_hide_natural_markup',
        '_start_pitch',
        '_widths',
        )

    _mutates_score = True

    _selector_type = 'logical ties'

    ### INITIALIZER ###

    def __init__(
        self,
        hide_flat_markup=None,
        hide_natural_markup=None,
        start_pitch=None,
        widths=None,
        ):
        assert isinstance(hide_flat_markup, (bool, type(None)))
        self._hide_flat_markup = hide_flat_markup
        assert isinstance(hide_natural_markup, (bool, type(None)))
        self._hide_natural_markup = hide_natural_markup
        if start_pitch is not None:
            start_pitch = pitchtools.NamedPitch(start_pitch)
        self._start_pitch = start_pitch
        if widths is not None:
            assert mathtools.all_are_nonnegative_integers(widths), repr(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls cluster specifier.

        Returns none.
        '''
        if self.widths is None:
            return
        widths = datastructuretools.CyclicTuple(self.widths)
        first_note = logical_ties[0].head
        root = inspect_(first_note).get_parentage().root
        with systemtools.ForbidUpdate(component=root):
            for index, logical_tie in enumerate(logical_ties):
                width = widths[index]
                for note in logical_tie:
                    self._make_cluster(note, width)

    ### PRIVATE METHODS ###

    def _make_cluster(self, note, width):
        if not width:
            return
        if self.start_pitch is not None:
            pitches = self._make_pitches(self.start_pitch, width)
        else:
            start_pitch = note.written_pitch
            pitches = self._make_pitches(start_pitch, width)
        chord = scoretools.Chord(pitches, note.written_duration)
        mutate(note).replace(chord)
        indicator = indicatortools.KeyCluster(
            include_black_keys=not self.hide_flat_markup,
            include_white_keys=not self.hide_natural_markup,
            )
        attach(indicator, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width-1):
            pitch = pitches[-1] + pitchtools.NamedInterval('M3')
            pitch = pitchtools.NamedPitch(pitch.diatonic_pitch_name)
            assert pitch.accidental.name == 'natural'
            pitches.append(pitch)
        return pitches

    ### PUBLIC PROPERTIES ###

    @property
    def hide_flat_markup(self):
        r'''Is true when cluster should hide flat markup.

        ..  container:: example

            **Example 1.** Hides flat markup:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4'),
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.tools.ClusterSpecifier(
                ...             hide_flat_markup=True,
                ...             widths=[3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_flat_markup

    @property
    def hide_natural_markup(self):
        r'''Is true when cluster should hide natural markup.

        ..  container:: example

            **Example 1.** Hides natural markup:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4'),
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.tools.ClusterSpecifier(
                ...             hide_natural_markup=True,
                ...             widths=[3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                                            \flat
                                        }
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
                                            \flat
                                        }
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
                                            \flat
                                        }
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
                                            \flat
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_natural_markup

    @property
    def start_pitch(self):
        r'''Gets start pitch of cluster.

        ..  container:: example

            **Example 1.** Takes start pitch from input notes:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.pitch.pitches('C4 D4 E4 F4'),
                ...         baca.tools.ClusterSpecifier(
                ...             widths=[3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <c' e' g'>2
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
                                <d' f' a'>4.
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
                                <e' g' b'>2
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
                            }
                        }
                    >>
                >>

        ..  container:: example

            **Example 2.** Sets start pitch explicitly:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.pitch.pitches('C4 D4 E4 F4'),
                ...         baca.tools.ClusterSpecifier(
                ...             start_pitch='G4',
                ...             widths=[3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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

            **Example 1.** Increasing widths:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4'),
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.tools.ClusterSpecifier(
                ...             widths=[0, 1, 2, 3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                                e'2
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>4.
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
                                <e' g'>2
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
                            }
                        }
                    >>
                >>

        ..  container:: example

            **Example 2.** Patterned widths:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.pitch.pitches('E4'),
                ...         baca.tools.ClusterSpecifier(
                ...             widths=[0, 3],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                                e'2
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
                                e'2
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
                            }
                        }
                    >>
                >>

        ..  container:: example

            **Example 3.** Leaves notes and chords unchanged:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
                ...     [
                ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
                ...         baca.pitch.pitches('E4'),
                ...         baca.tools.ClusterSpecifier(
                ...             widths=None,
                ...             ),
                ...         ],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> score = lilypond_file.score_block.items[0]
                >>> f(score)
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
                                e'2
                                e'4.
                                e'2
                                e'4.
                                \bar "|"
                            }
                        }
                    >>
                >>

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord should be left unchanged.

        Set to nonnegative integers or none.

        Returns nonnegative integers or none.
        '''
        return self._widths