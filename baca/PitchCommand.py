import abjad
import baca
import collections
import typing
from .Command import Command
from .Typing import Selector


class PitchCommand(Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_runs(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                g''8
                                [
            <BLANKLINE>
                                cs''!8
            <BLANKLINE>
                                ef''!8
            <BLANKLINE>
                                e''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                f''8
                                [
            <BLANKLINE>
                                b''8
            <BLANKLINE>
                                g''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                cs''!8
                                [
            <BLANKLINE>
                                ef''!8
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                f''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                b''8
                                [
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                cs''!8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_runs(),
        ...     baca.pitches('C4 F4 F#4 <B4 C#5> D5'), 
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                fs'!8
            <BLANKLINE>
                                <b' cs''!>8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                d''8
                                [
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                fs'!8
                                [
            <BLANKLINE>
                                <b' cs''!>8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                f'8
                                [
            <BLANKLINE>
                                fs'!8
            <BLANKLINE>
                                <b' cs''!>8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Large chord:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_runs(),
        ...     baca.pitches('<C4 D4 E4 F4 G4 A4 B4 C4>', allow_repeats=True)
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                <c' d' e' f' g' a' b'>8
                                [
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                <c' d' e' f' g' a' b'>8
                                [
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                <c' d' e' f' g' a' b'>8
                                [
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                <c' d' e' f' g' a' b'>8
                                [
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                                <c' d' e' f' g' a' b'>8
                                ]
            <BLANKLINE>
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
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_octaves',
        '_allow_repeats',
        '_cyclic',
        '_do_not_transpose',
        '_ignore_incomplete',
        '_mutated_score',
        '_persist',
        '_pitches',
        '_state',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_octaves: bool = None,
        allow_repeats: bool = None,
        cyclic: bool = None,
        do_not_transpose: bool = None,
        ignore_incomplete: bool = None,
        persist: str = None,
        pitches: typing.Iterable = None,
        selector: Selector = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if allow_octaves is not None:
            allow_octaves = bool(allow_octaves)
        self._allow_octaves = allow_octaves
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if cyclic is not None:
            cyclic = bool(cyclic)
        self._cyclic = cyclic
        if do_not_transpose is not None:
            do_not_transpose = bool(do_not_transpose)
        self._do_not_transpose = do_not_transpose
        if ignore_incomplete is not None:
            ignore_incomplete = bool(ignore_incomplete)
        self._ignore_incomplete = ignore_incomplete
        self._mutated_score = None
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        if pitches is not None:
            pitches = self._coerce_pitches(pitches)
        self._pitches = pitches
        self._state: abjad.OrderedDict = abjad.OrderedDict()

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.pitches:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
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
        previous_pitches_consumed = self._previous_pitches_consumed()
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        pitches_consumed = 0
        for i, plt in enumerate(plts):
            pitch = pitches[i + previous_pitches_consumed]
            new_plt = self._set_lt_pitch(plt, pitch)
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_octaves:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_OCTAVE, pleaf)
            if self.allow_repeats:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, pleaf)
            if self.do_not_transpose is True:
                for pleaf in plt:
                    abjad.attach(abjad.tags.DO_NOT_TRANSPOSE, pleaf)
            pitches_consumed += 1
        self._state = abjad.OrderedDict()
        pitches_consumed += previous_pitches_consumed
        self.state['pitches_consumed'] = pitches_consumed

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

    def _previous_pitches_consumed(self):
        dictionary = self.previous_segment_voice_metadata
        if not dictionary:
            return 0
        dictionary = dictionary.get(abjad.tags.PITCH, None)
        if not dictionary:
            return 0
        if dictionary.get('name') != self.persist:
            return 0
        pitches_consumed = dictionary.get('pitches_consumed', None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = self.previous_segment_voice_metadata
        dictionary = dictionary.get(abjad.tags.RHYTHM, None)
        if dictionary:
            if dictionary.get('incomplete_last_note', False):
                pitches_consumed -= 1
        return pitches_consumed

    @staticmethod
    def _set_lt_pitch(lt, pitch):
        new_lt = None
        for leaf in lt:
            abjad.detach(abjad.tags.NOT_YET_PITCHED, leaf)
        if pitch is None:
            if not lt.is_pitched:
                pass
            else:
                for leaf in lt:
                    rest = abjad.Rest(leaf.written_duration)
                    abjad.mutate(leaf).replace(rest, wrappers=True)
                new_lt = abjad.inspect(rest).get_logical_tie()
        elif isinstance(pitch, collections.Iterable):
            if isinstance(lt.head, abjad.Chord):
                for chord in lt:
                    chord.written_pitches = pitch
            else:
                assert isinstance(lt.head, (abjad.Note, abjad.Rest))
                for leaf in lt:
                    chord = abjad.Chord(pitch, leaf.written_duration)
                    abjad.mutate(leaf).replace(chord, wrappers=True)
                new_lt = abjad.inspect(chord).get_logical_tie()
        else:
            if isinstance(lt.head, abjad.Note):
                for note in lt:
                    note.written_pitch = pitch
            else:
                assert isinstance(lt.head, (abjad.Chord, abjad.Rest))
                for leaf in lt:
                    note = abjad.Note(pitch, leaf.written_duration)
                    abjad.mutate(leaf).replace(note, wrappers=True)
                new_lt = abjad.inspect(note).get_logical_tie()
        return new_lt

    ### PUBLIC PROPERTIES ###

    @property
    def allow_octaves(self) -> typing.Optional[bool]:
        """
        Is true when command allows octaves.
        """
        return self._allow_octaves

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when command allows repeat pitches.
        """
        return self._allow_repeats

    @property
    def cyclic(self) -> typing.Optional[bool]:
        """
        Is true when command reads pitches cyclically.
        """
        return self._cyclic

    @property
    def do_not_transpose(self) -> typing.Optional[bool]:
        """
        Is true when pitch escapes transposition.
        """
        return self._do_not_transpose

    @property
    def ignore_incomplete(self) -> typing.Optional[bool]:
        """
        Is true when persistent pitch command ignores previous segment
        incomplete last note.
        """
        return self._ignore_incomplete

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return abjad.tags.PITCH
        
    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def pitches(self) -> typing.Optional[typing.Iterable]:
        """
        Gets pitches.

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

        """
        return self._pitches

    @property
    def state(self) -> abjad.OrderedDict:
        """
        Gets state dictionary.
        """
        return self._state
