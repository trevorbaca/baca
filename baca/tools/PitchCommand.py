import abjad
import baca
import collections
from .Command import Command


class PitchCommand(Command):
    r'''Score pitch command.

    ..  container:: example

        With pitch numbers:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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
                                g''8 [
                                cs''8
                                ef''8
                                e''8 ]
                            }
                            {
                                f''8 [
                                b''8
                                g''8 ]
                            }
                            {
                                cs''8 [
                                ef''8
                                e''8
                                f''8 ]
                            }
                            {
                                b''8 [
                                g''8
                                cs''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        With pitch numbers:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches('C4 F4 F#4 <B4 C#5> D5'), 
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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
                                c'8 [
                                f'8
                                fs'8
                                <b' cs''>8 ]
                            }
                            {
                                d''8 [
                                c'8
                                f'8 ]
                            }
                            {
                                fs'8 [
                                <b' cs''>8
                                d''8
                                c'8 ]
                            }
                            {
                                f'8 [
                                fs'8
                                <b' cs''>8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Large chord:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches('<C4 D4 E4 F4 G4 A4 B4 C4>', repeats=True)
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ...     )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_repeat_pitches',
        '_cyclic',
        '_mutated_score',
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_repeat_pitches=None,
        cyclic=None,
        pitches=None,
        selector=None,
        ):
        Command.__init__(self, selector=selector)
        if allow_repeat_pitches is not None:
            allow_repeat_pitches = bool(allow_repeat_pitches)
        self._allow_repeat_pitches = allow_repeat_pitches
        if cyclic is not None:
            cyclic = bool(cyclic)
        self._cyclic = cyclic
        self._mutated_score = None
        if pitches is not None:
            pitches = self._coerce_pitches(pitches)
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if not self.pitches:
            return
        plts = []
        for pleaf in baca.select(argument).pleaves():
            plt = abjad.inspect(pleaf).get_logical_tie()
            if plt.head is pleaf:
                plts.append(plt)
        self._check_length(plts)
        pitches = self.pitches
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        for i, plt in enumerate(plts):
            pitch = pitches[i]
            new_plt = self._set_lt_pitch(plt, pitch)
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_repeat_pitches:
                for pleaf in plt:
                    abjad.attach('repeat pitch allowed', pleaf)

    ### PRIVATE METHODS ###

    def _check_length(self, plts):
        if self.cyclic:
            return
        if len(self.pitches) < len(plts):
            message = f'only {len(self.pitches)} pitches'
            message += f' for {len(plts)} logical ties:\n\n'
            message += f'{self!r} and {plts!r}.'
            raise Exception(message)

    @staticmethod
    def _coerce_pitches(pitches):
        if isinstance(pitches, str):
            pitches = PitchCommand._parse_string(pitches)
        items = []
        for item in pitches:
            if isinstance(item, str) and '<' in item and '>' in item:
                item = item.strip('<')
                item = item.strip('>')
                item = abjad.PitchSet(item, abjad.NamedPitch)
            elif isinstance(item, str):
                item = abjad.NamedPitch(item)
            elif isinstance(item, collections.Iterable):
                item = abjad.PitchSet(item, abjad.NamedPitch)
            else:
                item = abjad.NamedPitch(item)
            items.append(item)
        if isinstance(pitches, baca.Loop):
            pitches = type(pitches)(items=items, intervals=pitches.intervals)
        else:
            pitches = abjad.CyclicTuple(items)
        return pitches

    def _mutates_score(self):
        pitches = self.pitches or []
        if any(isinstance(_, collections.Iterable) for _ in pitches):
            return True
        return self._mutated_score

    @staticmethod
    def _parse_string(string):
        items, current_chord = [], []
        for part in string.split():
            if '<' in part:
                assert not current_chord
                current_chord.append(part)
            elif '>' in part:
                assert current_chord
                current_chord.append(part)
                item = ' '.join(current_chord)
                items.append(item)
                current_chord = []
            elif current_chord:
                current_chord.append(part)
            else:
                items.append(part)
        assert not current_chord, repr(current_chord)
        return items

    @staticmethod
    def _set_lt_pitch(lt, pitch):
        #mutated_score = False
        new_lt = None
        string = 'not yet pitched'
        for leaf in lt:
            abjad.detach(string, leaf)
        if pitch is None:
            if not lt.is_pitched:
                pass
            else:
                for leaf in lt:
                    rest = abjad.Rest(leaf.written_duration)
                    # TODO: overrides and indicators are lost!
                    abjad.mutate(leaf).replace(rest)
                    #mutated_score = True
                new_lt = abjad.inspect(rest).get_logical_tie()
        elif isinstance(pitch, collections.Iterable):
            if isinstance(lt.head, abjad.Chord):
                for chord in lt:
                    chord.written_pitches = pitch
            else:
                assert isinstance(lt.head, (abjad.Note, abjad.Rest))
                for leaf in lt:
                    chord = abjad.Chord(pitch, leaf.written_duration)
                    # TODO: overrides and indicators are lost!
                    abjad.mutate(leaf).replace(chord)
                    #mutated_score = True
                new_lt = abjad.inspect(chord).get_logical_tie()
        else:
            if isinstance(lt.head, abjad.Note):
                for note in lt:
                    note.written_pitch = pitch
            else:
                assert isinstance(lt.head, (abjad.Chord, abjad.Rest))
                for leaf in lt:
                    note = abjad.Note(pitch, leaf.written_duration)
                    # TODO: overrides and indicators are lost!
                    abjad.mutate(leaf).replace(note)
                    #mutated_score = True
                new_lt = abjad.inspect(note).get_logical_tie()
        #return mutated_score
        return new_lt

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeat_pitches(self):
        r'''Is true when command allows repeat pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_repeat_pitches

    @property
    def cyclic(self):
        r'''Is true when command reads pitches cyclically.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._cyclic

    @property
    def pitches(self):
        r'''Gets pitches.

        ..  container:: example

            Gets pitches:

            >>> command = baca.PitchCommand(
            ...     pitches=[19, 13, 15, 16, 17, 23],
            ...     )

            >>> for pitch in command.pitches:
            ...     pitch
            NamedPitch("g''")
            NamedPitch("cs''")
            NamedPitch("ef''")
            NamedPitch("e''")
            NamedPitch("f''")
            NamedPitch("b''")

        Defaults to none.

        Set to pitches or none.

        Returns pitches or none.
        '''
        return self._pitches
