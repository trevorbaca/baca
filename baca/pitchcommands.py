"""
Pitch functions.
"""
import collections
import dataclasses
import typing

import abjad

from . import command as _command
from . import pcollections as _pcollections
from . import select as _select
from .enums import enums as _enums


def _adjust_microtone_deviation_pitch(plt, deviation):
    assert deviation in (0.5, 0, -0.5)
    if deviation == 0:
        return
    for pleaf in plt:
        pitch = pleaf.written_pitch
        accidental = pitch.accidental.semitones + deviation
        pitch = abjad.NamedPitch(pitch, accidental=accidental)
        pleaf.written_pitch = pitch
        annotation = {"color microtone": True}
        abjad.attach(annotation, pleaf)


def _coerce_pitches(pitches):
    if isinstance(pitches, Loop):
        return pitches
    if isinstance(pitches, str):
        pitches = _parse_string(pitches)
    items = []
    for item in pitches:
        if isinstance(item, str) and "<" in item and ">" in item:
            item = item.strip("<")
            item = item.strip(">")
            item = set(abjad.NamedPitch(_) for _ in item.split())
        elif isinstance(item, str):
            item = abjad.NamedPitch(item)
        elif isinstance(item, collections.abc.Iterable):
            item = set(abjad.NamedPitch(_) for _ in item)
        else:
            item = abjad.NamedPitch(item)
        items.append(item)
    pitches = abjad.CyclicTuple(items)
    return pitches


def _do_cluster_command(
    argument, widths, *, direction=abjad.UP, hide_flat_markup=False, start_pitch=None
):
    if not argument:
        return False
    leaf = abjad.select.leaf(argument, 0)
    root = abjad.get.parentage(leaf).root
    widths = abjad.CyclicTuple(widths)
    with abjad.ForbidUpdate(component=root):
        chords = []
        for i, plt in enumerate(_select.plts(argument)):
            width = widths[i]
            chord = _make_cluster(
                plt,
                width,
                direction=direction,
                hide_flat_markup=hide_flat_markup,
                start_pitch=start_pitch,
            )
            chords.append(chord)
    return chords


def _do_interpolate_register_command(argument, start_pitch, stop_pitch):
    plts = _select.plts(argument)
    length = len(plts)
    for i, plt in enumerate(plts):
        registration = _get_registration(start_pitch, stop_pitch, i, length)
        for pleaf in plt:
            if isinstance(pleaf, abjad.Note):
                written_pitches = registration([pleaf.written_pitch])
                pleaf.written_pitch = written_pitches[0]
            elif isinstance(pleaf, abjad.Chord):
                written_pitches = registration(pleaf.written_pitches)
                pleaf.written_pitches = written_pitches
            else:
                raise TypeError(pleaf)
            abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)


def _do_microtone_deviation_command(argument, deviations):
    deviations = abjad.CyclicTuple(deviations)
    for i, plt in enumerate(_select.plts(argument)):
        deviation = deviations[i]
        _adjust_microtone_deviation_pitch(plt, deviation)
    return False


def _do_octave_displacement_command(argument, displacements):
    displacements = abjad.CyclicTuple(displacements)
    for i, plt in enumerate(_select.plts(argument)):
        displacement = displacements[i]
        interval = abjad.NumberedInterval(12 * displacement)
        for pleaf in plt:
            if isinstance(pleaf, abjad.Note):
                pitch = pleaf.written_pitch
                assert isinstance(pitch, abjad.NamedPitch)
                pitch += interval
                pleaf.written_pitch = pitch
            elif isinstance(pleaf, abjad.Chord):
                pitches = [_ + interval for _ in pleaf.written_pitches]
                pleaf.written_pitches = tuple(pitches)
            else:
                raise TypeError(pleaf)


def _do_pitch_command(
    argument,
    cyclic,
    pitches,
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_out_of_range: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    do_not_transpose: bool = False,
    mock: bool = False,
    previous_pitches_consumed: int = 0,
) -> tuple[int, bool]:
    assert isinstance(previous_pitches_consumed, int)
    pitches = _coerce_pitches(pitches)
    plts = []
    if allow_hidden:
        pleaves = _select.pleaves(argument)
    else:
        pleaves = _select.pleaves(argument, exclude=_enums.HIDDEN)
    for pleaf in pleaves:
        plt = abjad.get.logical_tie(pleaf)
        if plt.head is pleaf:
            plts.append(plt)
    if not cyclic:
        if len(pitches) < len(plts):
            message = f"only {len(pitches)} pitches"
            message += f" for {len(plts)} logical ties:\n\n"
            message += f"{pitches!r} and {plts!r}."
            raise Exception(message)
    if cyclic and not isinstance(pitches, abjad.CyclicTuple | Loop):
        pitches = abjad.CyclicTuple(pitches)
    pitches_consumed = 0
    mutated_score = False
    for i, plt in enumerate(plts):
        pitch = pitches[i + previous_pitches_consumed]
        new_plt = _set_lt_pitch(
            plt,
            pitch,
            allow_hidden=allow_hidden,
            allow_repitch=allow_repitch,
            mock=mock,
        )
        if new_plt is not None:
            mutated_score = True
            plt = new_plt
        if allow_octaves:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
        if allow_out_of_range:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
        if allow_repeats:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
        if do_not_transpose is True:
            for pleaf in plt:
                abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
        pitches_consumed += 1
    return pitches_consumed, mutated_score


def _do_register_command(argument, registration):
    plts = _select.plts(argument)
    assert isinstance(plts, list)
    for plt in plts:
        for pleaf in plt:
            if isinstance(pleaf, abjad.Note):
                pitch = pleaf.written_pitch
                pitches = registration([pitch])
                pleaf.written_pitch = pitches[0]
            elif isinstance(pleaf, abjad.Chord):
                pitches = pleaf.written_pitches
                pitches = registration(pitches)
                pleaf.written_pitches = pitches
            else:
                raise TypeError(pleaf)
            abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)


def _do_register_to_octave_command(argument, anchor, octave_number):
    pitches = abjad.iterate.pitches(argument)
    octave_adjustment = _pcollections.pitches_to_octave_adjustment(
        # pitches, anchor=self.anchor, octave_number=self.octave_number
        pitches,
        anchor=anchor,
        octave_number=octave_number,
    )
    pleaves = _select.pleaves(argument)
    for pleaf in pleaves:
        # self._set_pitch(pleaf, lambda _: _.transpose(n=12 * octave_adjustment))
        _set_pitch(pleaf, lambda _: _.transpose(n=12 * octave_adjustment))


def _do_staff_position_command(
    argument,
    numbers,
    *,
    allow_hidden=False,
    allow_out_of_range=False,
    allow_repitch=False,
    exact=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    numbers = abjad.CyclicTuple(numbers)
    plt_count = 0
    mutated_score = False
    for i, plt in enumerate(_select.plts(argument)):
        clef = abjad.get.effective(
            plt.head,
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        number = numbers[i]
        # TODO: remove branch because never used?
        if isinstance(number, list):
            raise Exception("ASDF")
            positions = [abjad.StaffPosition(_) for _ in number]
            pitches = [clef.to_pitch(_) for _ in positions]
            new_lt = _set_lt_pitch(
                plt,
                pitches,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                set_chord_pitches_equal=set_chord_pitches_equal,
            )
            if new_lt is not None:
                mutated_score = True
                plt = new_lt
        else:
            position = abjad.StaffPosition(number)
            pitch = clef.to_pitch(position)
            new_lt = _set_lt_pitch(
                plt,
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                set_chord_pitches_equal=set_chord_pitches_equal,
            )
            if new_lt is not None:
                mutated_score = True
                plt = new_lt
        plt_count += 1
        for pleaf in plt:
            abjad.attach(_enums.STAFF_POSITION, pleaf)
            if allow_out_of_range:
                abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
            abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
            abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
    if exact and plt_count != len(numbers):
        message = f"PLT count ({plt_count}) does not match"
        message += f" staff position count ({len(numbers)})."
        raise Exception(message)
    return mutated_score


def _do_staff_position_interpolation_command(
    argument,
    start,
    stop,
    *,
    allow_hidden=False,
    mock=False,
    pitches_instead_of_staff_positions=False,
):
    plts = _select.plts(argument)
    if not plts:
        return False
    count = len(plts)
    if isinstance(start, abjad.StaffPosition):
        start_staff_position = start
    else:
        start_phead = plts[0].head
        clef = abjad.get.effective(start_phead, abjad.Clef)
        start_staff_position = clef.to_staff_position(start)
    if isinstance(stop, abjad.StaffPosition):
        stop_staff_position = stop
    else:
        stop_phead = plts[-1].head
        clef = abjad.get.effective(
            stop_phead,
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        stop_staff_position = clef.to_staff_position(stop)
    unit_distance = abjad.Fraction(
        stop_staff_position.number - start_staff_position.number, count - 1
    )
    for i, plt in enumerate(plts):
        staff_position = unit_distance * i + start_staff_position.number
        staff_position = round(staff_position)
        staff_position = abjad.StaffPosition(staff_position)
        clef = abjad.get.effective(
            plt.head,
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        pitch = clef.to_pitch(staff_position)
        new_lt = _set_lt_pitch(
            plt,
            pitch,
            allow_hidden=allow_hidden,
            allow_repitch=True,
            mock=mock,
        )
        assert new_lt is None, repr(new_lt)
        for leaf in plt:
            abjad.attach(_enums.ALLOW_REPEAT_PITCH, leaf)
            if not pitches_instead_of_staff_positions:
                abjad.attach(_enums.STAFF_POSITION, leaf)
    if isinstance(start, abjad.NamedPitch):
        start_pitch = start
    else:
        assert isinstance(start, abjad.StaffPosition)
        clef = abjad.get.effective(
            plts[0],
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        start_pitch = clef.to_pitch(start)
    new_lt = _set_lt_pitch(
        plts[0],
        start_pitch,
        allow_hidden=allow_hidden,
        allow_repitch=True,
        mock=mock,
    )
    assert new_lt is None, repr(new_lt)
    if isinstance(stop, abjad.NamedPitch):
        stop_pitch = stop
    else:
        assert isinstance(stop, abjad.StaffPosition)
        clef = abjad.get.effective(
            plts[0],
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        stop_pitch = clef.to_pitch(stop)
    new_lt = _set_lt_pitch(
        plts[-1],
        stop_pitch,
        allow_hidden=allow_hidden,
        allow_repitch=True,
        mock=mock,
    )
    assert new_lt is None, repr(new_lt)
    return False


def _get_registration(start_pitch, stop_pitch, i, length):
    start_pitch = start_pitch.number
    stop_pitch = stop_pitch.number
    compass = stop_pitch - start_pitch
    fraction = abjad.Fraction(i, length)
    addendum = fraction * compass
    current_pitch = start_pitch + addendum
    current_pitch = int(current_pitch)
    return _pcollections.Registration(
        [
            _pcollections.RegistrationComponent(
                abjad.PitchRange("[A0, C8]"), abjad.NumberedPitch(current_pitch)
            )
        ]
    )


def _make_cluster(
    plt, width, *, direction=abjad.UP, hide_flat_markup=False, start_pitch=None
):
    assert plt.is_pitched, repr(plt)
    assert isinstance(width, int), repr(width)
    if start_pitch is None:
        start_pitch = plt.head.written_pitch
    pitches = _make_cluster_pitches(start_pitch, width)
    key_cluster = abjad.KeyCluster(include_flat_markup=(not hide_flat_markup))
    for pleaf in plt:
        chord = abjad.Chord(pitches, pleaf.written_duration)
        wrappers = abjad.get.wrappers(pleaf)
        abjad.detach(object, pleaf)
        for wrapper in wrappers:
            abjad.attach(wrapper, chord, direction=wrapper.direction)
        abjad.mutate.replace(pleaf, chord)
        abjad.attach(key_cluster, chord, direction=direction)
        abjad.attach(_enums.ALLOW_REPEAT_PITCH, chord)
        abjad.detach(_enums.NOT_YET_PITCHED, chord)
    return chord


def _make_cluster_pitches(start_pitch, width):
    pitches = [start_pitch]
    for i in range(width - 1):
        pitch = pitches[-1] + abjad.NamedInterval("M3")
        pitch = abjad.NamedPitch(pitch, accidental="natural")
        assert pitch.accidental == abjad.Accidental("natural")
        pitches.append(pitch)
    return pitches


def _parse_string(string):
    items, current_chord = [], []
    for part in string.split():
        if "<" in part:
            assert not current_chord
            current_chord.append(part)
        elif ">" in part:
            assert current_chord
            current_chord.append(part)
            item = " ".join(current_chord)
            items.append(item)
            current_chord = []
        elif current_chord:
            current_chord.append(part)
        else:
            items.append(part)
    assert not current_chord, repr(current_chord)
    return items


def _previous_pitches_consumed(dictionary, persist, *, ignore_incomplete=False):
    if not dictionary:
        return 0
    dictionary = dictionary.get(_enums.PITCH.name, None)
    if not dictionary:
        return 0
    if dictionary.get("name") != persist:
        return 0
    pitches_consumed = dictionary.get("pitches_consumed", None)
    if not pitches_consumed:
        return 0
    assert 1 <= pitches_consumed
    if ignore_incomplete:
        return pitches_consumed
    dictionary = dictionary.get(_enums.RHYTHM.name, None)
    if dictionary:
        if dictionary.get("incomplete_final_note", False):
            pitches_consumed -= 1
    return pitches_consumed


def _set_lt_pitch(
    lt,
    pitch,
    *,
    allow_hidden=False,
    allow_repitch=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    new_lt = None
    already_pitched = _enums.ALREADY_PITCHED
    for leaf in lt:
        if not allow_hidden and abjad.get.has_indicator(leaf, _enums.HIDDEN):
            continue
        abjad.detach(_enums.NOT_YET_PITCHED, leaf)
        if mock is True:
            abjad.attach(_enums.MOCK, leaf)
        if allow_repitch:
            continue
        if abjad.get.has_indicator(leaf, already_pitched):
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if voice is None:
                name = "no voice"
            else:
                name = voice.name
            raise Exception(f"already pitched {repr(leaf)} in {name}.")
        abjad.attach(already_pitched, leaf)
    if pitch is None:
        if not lt.is_pitched:
            pass
        else:
            for leaf in lt:
                rest = abjad.Rest(leaf.written_duration, multiplier=leaf.multiplier)
                abjad.mutate.replace(leaf, rest, wrappers=True)
            new_lt = abjad.get.logical_tie(rest)
    elif isinstance(pitch, collections.abc.Iterable):
        if isinstance(lt.head, abjad.Chord):
            for chord in lt:
                chord.written_pitches = pitch
        else:
            assert isinstance(lt.head, abjad.Note | abjad.Rest)
            for leaf in lt:
                chord = abjad.Chord(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, chord, wrappers=True)
            new_lt = abjad.get.logical_tie(chord)
    else:
        if isinstance(lt.head, abjad.Note):
            for note in lt:
                note.written_pitch = pitch
        elif set_chord_pitches_equal is True and isinstance(lt.head, abjad.Chord):
            for chord in lt:
                for note_head in chord.note_heads:
                    note_head.written_pitch = pitch
        else:
            assert isinstance(lt.head, abjad.Chord | abjad.Rest)
            for leaf in lt:
                note = abjad.Note(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, note, wrappers=True)
            new_lt = abjad.get.logical_tie(note)
    return new_lt


def _set_pitch(leaf, transposition):
    if isinstance(leaf, abjad.Note):
        pitch = transposition(leaf.written_pitch)
        leaf.written_pitch = pitch
    elif isinstance(leaf, abjad.Chord):
        pitches = [transposition(_) for _ in leaf.written_pitches]
        leaf.written_pitches = pitches
    abjad.detach(_enums.NOT_YET_REGISTERED, leaf)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ClusterCommand(_command.Command):
    r"""
    Cluster command.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.replace_with_clusters([3, 4]),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        \time 9/16
                        <c' e' g'>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a' c''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <bf' d'' f''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <fs'' a'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'' g'' b''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <ef'' g'' b'' d'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <af'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g'' b'' d''' f'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <a' c'' e''>16
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                }
            >>

    ..  container:: example

        Hides flat markup:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )


        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.natural_clusters(widths=[3]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                    }
                >>
            }

    ..  container:: example

        Takes start pitch from input notes:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )


        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.replace_with_clusters([3]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <c' e' g'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <f' a' c''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Sets start pitch explicitly:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.replace_with_clusters([3], start_pitch="G4"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Increasing widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.replace_with_clusters([1, 2, 3, 4], start_pitch="E4"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Patterned widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.replace_with_clusters([1, 3], start_pitch="E4"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Leaves notes and chords unchanged:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.replace_with_clusters([]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }
                >>
            }

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

    """

    direction: abjad.Vertical | None = abjad.UP
    hide_flat_markup: bool = False
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN)
    start_pitch: abjad.NamedPitch | None = None
    widths: typing.Sequence[int] | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.hide_flat_markup, bool), repr(self.hide_flat_markup)
        if self.start_pitch is not None:
            assert isinstance(self.start_pitch, abjad.NamedPitch), repr(
                self.start_pitch
            )
        assert abjad.math.all_are_nonnegative_integers(self.widths)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.widths:
            return False
        if self.selector:
            argument = self.selector(argument)
        chords = _do_cluster_command(
            argument,
            self.widths,
            direction=self.direction,
            hide_flat_markup=self.hide_flat_markup,
            start_pitch=self.start_pitch,
        )
        return bool(chords)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class DiatonicClusterCommand(_command.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        True

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    widths: typing.Sequence[int] = ()
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        assert all(isinstance(_, int) for _ in self.widths), repr(self.widths)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.widths:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        widths = abjad.CyclicTuple(self.widths)
        for i, plt in enumerate(_select.plts(argument)):
            width = widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            change = abjad.pitch._diatonic_pc_number_to_pitch_class_number
            numbers_ = [(12 * (_ // 7)) + change[_ % 7] for _ in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers_]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate.replace(pleaf, chord)
        return True

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Loop:
    """
    Loop.

    ..  container:: example

        >>> loop = baca.Loop([0, 2, 4], [1])
        >>> loop
        Loop(pitches=[0, 2, 4], intervals=[1])

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

    """

    pitches: typing.Sequence[int]
    intervals: typing.Sequence[int]

    def __post_init__(self):
        assert all(isinstance(_, int) for _ in self.pitches), self.pitches
        assert all(isinstance(_, int) for _ in self.intervals), self.intervals

    def __getitem__(self, i: int) -> abjad.NamedPitch:
        assert isinstance(i, int), repr(i)
        intervals = abjad.CyclicTuple(self.intervals)
        pitches = abjad.CyclicTuple(self.pitches)
        iteration = i // len(pitches)
        if not pitches:
            transposition = 0
        else:
            transposition = sum(intervals[:iteration])
        number = pitches[i]
        pitch = abjad.NamedPitch(number + transposition)
        return pitch

    def __iter__(self):
        return self.pitches.__iter__()


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class MicrotoneDeviationCommand(_command.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("E4"),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        eqs'8
                        e'8
                        eqf'8
                        ]
                        e'8
                        [
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        ]
                    }
                >>
            }

    """

    deviations: typing.Sequence[int | float] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert all(isinstance(_, int | float) for _ in self.deviations)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.deviations:
            return False
        if self.selector:
            argument = self.selector(argument)
        _do_microtone_deviation_command(argument, self.deviations)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OctaveDisplacementCommand(_command.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.suite(
        ...         baca.pitch("G4"),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g'8
                        [
                        g'8
                        g''8
                        g''8
                        ]
                        g'8
                        [
                        g'8
                        g8
                        ]
                        g8
                        [
                        g'''8
                        g'''8
                        g'8
                        ]
                        g'8
                        [
                        g''8
                        g''8
                        ]
                    }
                >>
            }

    """

    displacements: typing.Sequence[int] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert self._is_octave_displacement_vector(self.displacements)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.displacements is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        _do_octave_displacement_command(argument, self.displacements)
        return False

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, tuple | list):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PitchCommand(_command.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g''8
                        [
                        cs''8
                        ef''8
                        e''8
                        ]
                        f''8
                        [
                        b''8
                        g''8
                        ]
                        cs''8
                        [
                        ef''8
                        e''8
                        f''8
                        ]
                        b''8
                        [
                        g''8
                        cs''8
                        ]
                    }
                >>
            }

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("C4 F4 F#4 <B4 C#5> D5"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        c'8
                        [
                        f'8
                        fs'8
                        <b' cs''>8
                        ]
                        d''8
                        [
                        c'8
                        f'8
                        ]
                        fs'8
                        [
                        <b' cs''>8
                        d''8
                        c'8
                        ]
                        f'8
                        [
                        fs'8
                        <b' cs''>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Large chord:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("<C4 D4 E4 F4 G4 A4 B4 C4>", allow_repeats=True)
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ... )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

    allow_hidden: bool = False
    allow_octaves: bool = False
    allow_out_of_range: bool = False
    allow_repeats: bool = False
    allow_repitch: bool = False
    mock: bool = False
    cyclic: bool = False
    do_not_transpose: bool = False
    ignore_incomplete: bool = False
    persist: str = ""
    pitches: typing.Sequence | Loop = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.allow_octaves, bool), repr(self.allow_octaves)
        assert isinstance(self.allow_out_of_range, bool), repr(self.allow_out_of_range)
        assert isinstance(self.allow_repeats, bool), repr(self.allow_repeats)
        assert isinstance(self.allow_repitch, bool), repr(self.allow_repitch)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.cyclic, bool), repr(self.cyclic)
        assert isinstance(self.do_not_transpose, bool), repr(self.do_not_transpose)
        assert isinstance(self.ignore_incomplete, bool), repr(self.ignore_incomplete)
        assert isinstance(self.persist, str), repr(self.persist)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.pitches:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        previous_pitches_consumed = self._previous_pitches_consumed(runtime)
        pitches = _coerce_pitches(self.pitches)
        pitches_consumed, mutated_score = _do_pitch_command(
            argument,
            self.cyclic,
            pitches,
            allow_hidden=self.allow_hidden,
            allow_octaves=self.allow_octaves,
            allow_out_of_range=self.allow_out_of_range,
            allow_repeats=self.allow_repeats,
            allow_repitch=self.allow_repitch,
            do_not_transpose=self.do_not_transpose,
            mock=self.mock,
            previous_pitches_consumed=previous_pitches_consumed,
        )
        pitches_consumed += previous_pitches_consumed
        self.state["pitches_consumed"] = pitches_consumed
        return mutated_score

    def _previous_pitches_consumed(self, runtime):
        assert isinstance(runtime, dict), repr(runtime)
        dictionary = runtime.get("previous_section_voice_metadata", None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(_enums.PITCH.name, None)
        if not dictionary:
            return 0
        if dictionary.get("name") != self.persist:
            return 0
        pitches_consumed = dictionary.get("pitches_consumed", None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = runtime["previous_section_voice_metadata"]
        dictionary = dictionary.get(_enums.RHYTHM.name, None)
        if dictionary:
            if dictionary.get("incomplete_final_note", False):
                pitches_consumed -= 1
        return pitches_consumed

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return _enums.PITCH.name

    @property
    def state(self):
        """
        Gets state dictionary.
        """
        return self._state


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterCommand(_command.Command):
    r"""
    Register command.

    ..  container:: example

        With music-accumulator:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [baca.RegistrationComponent(
        ...                 abjad.PitchRange("[A0, C8]"), abjad.NumberedPitch(15)
        ...             )],
        ...         ),
        ...     ),
        ... )
        >>> selection = stack([[10, 12, 14], [10, 12, 14], [10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With section-accumulator:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4"),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [baca.RegistrationComponent(
        ...                 abjad.PitchRange("[A0, C8]"), abjad.NumberedPitch(15)
        ...             )],
        ...         ),
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [baca.RegistrationComponent(
        ...                 abjad.PitchRange("[A0, C8]"), abjad.NumberedPitch(-6)
        ...             )],
        ...         ),
        ...     ),
        ... )
        >>> selection = stack([{10, 12, 14}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <bf c' d'>16
                    }
                }
            >>

    """

    registration: _pcollections.Registration | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = _pcollections.Registration
        assert isinstance(self.registration, prototype), repr(self.registration)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.registration is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        _do_register_command(argument, self.registration)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterInterpolationCommand(_command.Command):
    r"""
    Register interpolation command.

    ..  container:: example

        With music-accumulator:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c''16
                        b'16
                        af'16
                        g''16
                        cs''16
                        d''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        f''16
                        a''16
                        bf''16
                        c'''16
                        b''16
                        af''16
                        g'''16
                        cs'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ... ]
        >>> collections = [set(_) for _ in collections]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/8
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <cs''' d'''>16
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, 12),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf''8
                        c''8
                        ]
                        b''8
                        [
                        af''8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs''8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a''8
                        bf''8
                        ]
                        c''8
                        [
                        b''8
                        af''8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, 0),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d'8
                        fs'8
                        ]
                        e'8
                        [
                        ef'8
                        f'8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(0, 12),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs'8
                        [
                        e'8
                        ef'8
                        f'8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, -12),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf8
                        ]
                        c'8
                        [
                        b8
                        af8
                        ]
                        g8
                        [
                        cs'8
                        d'8
                        fs8
                        ]
                        e8
                        [
                        ef8
                        f8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(accumulator.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> accumulator(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(-12, 12),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs8
                        [
                        e8
                        ef8
                        f8
                        ]
                        a8
                        [
                        bf8
                        c'8
                        ]
                        b8
                        [
                        af8
                        g'8
                        cs'8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Selects tuplet 0:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.tuplet(_, 0),
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, 0),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Selects tuplet -1:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.tuplet(_, -1),
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, -1),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        Maps to tuplets:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         selector=lambda _: abjad.select.tuplets(_)
        ...     ),
        ...     baca.new(
        ...         baca.register(0, 24),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        ef''16
                        \abjad-color-music #'red
                        f''16
                        \abjad-color-music #'red
                        a'16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        c''16
                        \abjad-color-music #'red
                        b''16
                        \abjad-color-music #'red
                        af''16
                        \abjad-color-music #'red
                        g''16
                        \abjad-color-music #'red
                        cs'''16
                        \abjad-color-music #'red
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        fs'16
                        [
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'blue
                        f''16
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'blue
                        c''16
                        \abjad-color-music #'blue
                        b''16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'blue
                        g''16
                        \abjad-color-music #'blue
                        cs'''16
                        \abjad-color-music #'blue
                        d'''16
                        ]
                    }
                }
            >>

    """

    start_pitch: abjad.NumberedPitch = abjad.NumberedPitch(0)
    stop_pitch: abjad.NumberedPitch = abjad.NumberedPitch(0)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.start_pitch, abjad.NumberedPitch), repr(self.start_pitch)
        assert isinstance(self.stop_pitch, abjad.NumberedPitch), repr(self.stop_pitch)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        _do_interpolate_register_command(argument, self.start_pitch, self.stop_pitch)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterToOctaveCommand(_command.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c' d'' e'''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c d' e''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c, d e'>16
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c'16
                        [
                        d''16
                        e'''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c16
                        [
                        d'16
                        e''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c,16
                        [
                        d16
                        e'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf'16
                        [
                        c''16
                        d''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Bass anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.DOWN,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    ..  container:: example

        Center anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.CENTER,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        Soprano anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.UP,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> staff = abjad.Staff([chord])
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            \clef "bass"
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=1)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c,, d, e>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=2)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=3)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=4)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=5)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    """

    anchor: abjad.Vertical = abjad.DOWN
    octave_number: int | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (abjad.CENTER, abjad.DOWN, abjad.UP)
        assert self.anchor in prototype, repr(self.anchor)
        assert isinstance(self.octave_number, int), repr(self.octave_number)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if self.selector:
            argument = self.selector(argument)
        _do_register_to_octave_command(
            argument, anchor=self.anchor, octave_number=self.octave_number
        )
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffPositionCommand(_command.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("percussion"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    numbers: typing.Sequence[int | list | abjad.StaffPosition] = ()
    allow_hidden: bool = False
    allow_out_of_range: bool = False
    allow_repitch: bool = False
    exact: bool = False
    mock: bool = False
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN)
    set_chord_pitches_equal: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (int, list, abjad.StaffPosition)
        assert all(isinstance(_, prototype) for _ in self.numbers), repr(self.numbers)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.allow_out_of_range, bool), repr(self.allow_out_of_range)
        assert isinstance(self.allow_repitch, bool), repr(self.allow_repitch)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.exact, bool), repr(self.exact)
        assert isinstance(self.set_chord_pitches_equal, bool), repr(
            self.set_chord_pitches_equal
        )

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.numbers:
            return False
        if self.selector:
            argument = self.selector(argument)
        numbers = abjad.CyclicTuple(self.numbers)
        mutated_score = _do_staff_position_command(
            argument,
            numbers,
            allow_hidden=self.allow_hidden,
            allow_out_of_range=self.allow_out_of_range,
            allow_repitch=self.allow_repitch,
            exact=self.exact,
            set_chord_pitches_equal=self.set_chord_pitches_equal,
        )
        return mutated_score


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffPositionInterpolationCommand(_command.Command):

    start: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    stop: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    allow_hidden: bool = False
    mock: bool = False
    pitches_instead_of_staff_positions: bool = False
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (abjad.NamedPitch, abjad.StaffPosition)
        if isinstance(self.start, str):
            self.start = abjad.NamedPitch(self.start)
        elif isinstance(self.start, int):
            self.start = abjad.StaffPosition(self.start)
        assert isinstance(self.start, prototype), repr(self.start)
        if isinstance(self.stop, str):
            self.stop = abjad.NamedPitch(self.stop)
        elif isinstance(self.stop, int):
            self.stop = abjad.StaffPosition(self.stop)
        assert isinstance(self.stop, prototype), repr(self.stop)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.pitches_instead_of_staff_positions, bool)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        _do_staff_position_interpolation_command(
            argument,
            self.start,
            self.stop,
            allow_hidden=self.allow_hidden,
            mock=self.mock,
            pitches_instead_of_staff_positions=self.pitches_instead_of_staff_positions,
        )
        return False


def bass_to_octave(
    n: int,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire selection appears
        in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(3),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.plts(_),
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f'8
                        [
                        ~
                        \abjad-color-music #'green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef' e' fs''>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a8
                        [
                        ~
                        \abjad-color-music #'green
                        a32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(selector=lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.DOWN, octave_number=n, selector=selector
    )


def bass_to_octave_function(argument, n: int) -> None:
    _do_register_to_octave_command(argument, anchor=abjad.DOWN, octave_number=n)


def center_to_octave(
    n: int,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.center_to_octave(3),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.plts(_),
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c, d, bf,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c, d, bf,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f8
                        [
                        ~
                        \abjad-color-music #'green
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(selector=lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.CENTER, octave_number=n, selector=selector
    )


def deviation(
    deviations: list[int | float],
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> MicrotoneDeviationCommand:
    return MicrotoneDeviationCommand(deviations=deviations, selector=selector)


def deviation_function(
    argument,
    deviations: list[int | float],
) -> None:
    _do_microtone_deviation_command(argument, deviations)


def diatonic_clusters(
    widths: list[int],
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> DiatonicClusterCommand:
    return DiatonicClusterCommand(selector=selector, widths=widths)


def displacement(
    displacements: list[int],
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack(3 * [[0, 2, 3]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 27/16
                        r8
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        c16
                        [
                        d''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/12
                    {
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ... )
        >>> selection = stack(6 * [{0, 2, 3}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 15/8
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(displacements=displacements, selector=selector)


def displacement_function(argument, displacements: list[int]) -> None:
    _do_octave_displacement_command(argument, displacements)


def interpolate_pitches(
    start: int | str | abjad.NamedPitch,
    stop: int | str | abjad.NamedPitch,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from staff position of ``start`` pitch to staff position of ``stop``
    pitch.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 0)),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        fs''16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 0)),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ...     baca.glissando(
        ...         allow_repeats=True,
        ...         hide_middle_note_heads=True,
        ...     ),
        ...     baca.glissando_thickness(3),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \override Glissando.thickness = 3
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        \glissando
                        \hide NoteHead
                        \override Accidental.stencil = ##f
                        \override NoteColumn.glissando-skip = ##t
                        \override NoteHead.no-ledgers = ##t
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        \revert Accidental.stencil
                        \revert NoteColumn.glissando-skip
                        \revert NoteHead.no-ledgers
                        \undo \hide NoteHead
                        fs''16
                        ]
                        \revert Glissando.thickness
                    }
                }
            >>

    """
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        allow_hidden=allow_hidden,
        mock=mock,
        pitches_instead_of_staff_positions=True,
        selector=selector,
    )


def interpolate_pitches_function(
    argument,
    start: int | str | abjad.NamedPitch,
    stop: int | str | abjad.NamedPitch,
    *,
    allow_hidden: bool = False,
    mock: bool = False,
) -> None:
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    _do_staff_position_interpolation_command(
        argument,
        start_,
        stop_,
        allow_hidden=allow_hidden,
        mock=mock,
        pitches_instead_of_staff_positions=True,
    )


# TODO: change naming
_interpolate_pitches_function = interpolate_pitches


def interpolate_staff_positions(
    start: int | abjad.StaffPosition,
    stop: int | abjad.StaffPosition,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    """
    Interpolates from ``start`` staff position to ``stop`` staff position.
    """
    if isinstance(start, abjad.StaffPosition):
        start_ = start
    else:
        start_ = abjad.StaffPosition(start)
    if isinstance(stop, abjad.StaffPosition):
        stop_ = stop
    else:
        stop_ = abjad.StaffPosition(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        allow_hidden=allow_hidden,
        mock=mock,
        selector=selector,
    )


_interpolate_staff_positions_function = interpolate_staff_positions


def natural_clusters(
    widths: typing.Sequence[int],
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    if start_pitch is not None:
        start_pitch = abjad.NamedPitch(start_pitch)
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
    )


def pitch(
    pitch,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    persist: str = "",
) -> PitchCommand:
    r"""
    Makes pitch command.

    ..  container:: example

        REGRESSION. Preserves duration multipliers when leaves cast from one type to
        another (note to chord in this example):

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> stack = rmakers.stack(
        ...     rmakers.note(),
        ...     rmakers.written_duration(1),
        ... )
        >>> music = stack(accumulator.get())
        >>> score["Music"].extend(music)

        >>> accumulator(
        ...     "Music",
        ...     baca.pitch("<C4 D4 E4>"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    """
    if isinstance(pitch, list | tuple) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    if allow_out_of_range not in (None, True, False):
        raise Exception(
            f"allow_out_of_range must be boolean (not {allow_out_of_range!r})."
        )
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        mock=mock,
        persist=persist,
        pitches=[pitch],
        selector=selector,
    )


def pitch_function(
    argument,
    pitch,
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
) -> bool:
    assert isinstance(pitch, str | list | tuple | abjad.Pitch), repr(pitch)
    if isinstance(pitch, list | tuple) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    assert isinstance(allow_out_of_range, bool), repr(allow_out_of_range)
    assert isinstance(do_not_transpose, bool), repr(do_not_transpose)
    cyclic = True
    result = _do_pitch_command(
        argument,
        cyclic,
        [pitch],
        allow_hidden=allow_hidden,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        do_not_transpose=do_not_transpose,
        mock=mock,
    )
    pitches_consumed, mutated_score = result
    return mutated_score


# TODO: rename
_pitch_command_factory = pitch


def pitches(
    pitches,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    exact: bool = False,
    ignore_incomplete: bool = False,
    persist: str = "",
) -> PitchCommand:
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_hidden=allow_hidden,
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        mock=mock,
        persist=persist,
        pitches=pitches,
        selector=selector,
    )


# TODO: rename
_pitches_command_factory = pitches


def pitches_function(
    argument,
    pitches,
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    metadata: dict = None,
    mock: bool = False,
    do_not_transpose: bool = False,
    exact: bool = False,
    ignore_incomplete: bool = False,
    persist: str = "",
) -> bool:
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if metadata is not None:
        assert isinstance(metadata, dict), repr(metadata)
        assert persist, repr(persist)
    assert isinstance(persist, str), repr(persist)
    previous_pitches_consumed = 0
    if persist:
        assert isinstance(metadata, dict), repr(metadata)
        previous_pitches_consumed = _previous_pitches_consumed(
            metadata, persist, ignore_incomplete=ignore_incomplete
        )
    result = _do_pitch_command(
        argument,
        cyclic,
        pitches,
        allow_hidden=allow_hidden,
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        do_not_transpose=do_not_transpose,
        mock=mock,
        previous_pitches_consumed=previous_pitches_consumed,
    )
    pitches_consumed, mutated_score = result
    if persist:
        pitches_consumed += previous_pitches_consumed
        assert isinstance(metadata, dict), repr(metadata)
        dictionary = {"name": persist, "pitches_consumed": pitches_consumed}
        metadata.setdefault("PITCH", {})
        metadata["PITCH"].update(dictionary)
    return mutated_score


def register(
    start: int,
    stop: int = None,
    *,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterCommand | RegisterInterpolationCommand:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf4
                        ~
                        bf16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs16
                        [
                        e'16
                        ]
                        ef'4
                        ~
                        ef'16
                        r16
                        af16
                        [
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
        ...     baca.register(
        ...         -6,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af16
                        [
                        \abjad-color-music #'green
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6, 18),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs'16
                        [
                        e'16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a''16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
        ...     baca.register(
        ...         -6, 18,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af'16
                        [
                        \abjad-color-music #'green
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    start_pitch, stop_pitch = register_prepare(start, stop)
    if stop_pitch is None:
        return RegisterCommand(
            registration=_pcollections.Registration(
                [
                    _pcollections.RegistrationComponent(
                        abjad.PitchRange("[A0, C8]"), start_pitch
                    )
                ]
            ),
            selector=selector,
        )
    return RegisterInterpolationCommand(
        selector=selector, start_pitch=start_pitch, stop_pitch=stop_pitch
    )


def register_function(
    argument,
    start: int,
    stop: int = None,
) -> None:
    assert not isinstance(argument, int), repr(argument)
    start_pitch, stop_pitch = register_prepare(start, stop)
    if stop_pitch is None:
        registration = _pcollections.Registration(
            [
                _pcollections.RegistrationComponent(
                    abjad.PitchRange("[A0, C8]"), abjad.NumberedPitch(start_pitch)
                )
            ]
        )
        _do_register_command(argument, registration)
    else:
        _do_interpolate_register_command(argument, start_pitch, stop_pitch)


def register_prepare(start, stop):
    if start is not None:
        start_pitch = abjad.NumberedPitch(start)
    if stop is not None:
        stop_pitch = abjad.NumberedPitch(stop)
    else:
        stop_pitch = None
    return start_pitch, stop_pitch


def replace_with_clusters(
    widths: list[int],
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    if start_pitch is not None:
        start_pitch = abjad.NamedPitch(start_pitch)
    return ClusterCommand(selector=selector, start_pitch=start_pitch, widths=widths)


def replace_with_clusters_function(
    argument,
    widths: list[int],
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> list[abjad.Chord]:
    if start_pitch is not None:
        start_pitch = abjad.NamedPitch(start_pitch)
    chords = _do_cluster_command(argument, widths, start_pitch=start_pitch)
    assert all(isinstance(_, abjad.Chord) for _ in chords)
    return chords


def soprano_to_octave(
    n: int,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the collection of all PLTs
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lone=True,
        ...         selector=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.soprano_to_octave(3),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c,, d,, bf,,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c,, d,, bf,,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f,8
                        [
                        ~
                        \abjad-color-music #'green
                        f,32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g,, af,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g,, af,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each pitched logical
        tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(selector=lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(anchor=abjad.UP, octave_number=n, selector=selector)


def staff_position(
    argument: int | list | abjad.StaffPosition,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    set_chord_pitches_equal: bool = False,
) -> StaffPositionCommand:
    assert isinstance(argument, int | list | abjad.StaffPosition), repr(argument)
    if isinstance(argument, list):
        assert all(isinstance(_, int | abjad.StaffPosition) for _ in argument)
    return StaffPositionCommand(
        numbers=[argument],
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repitch=allow_repitch,
        mock=mock,
        selector=selector,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )


def staff_position_function(
    argument,
    numbers: int | list | abjad.StaffPosition,
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    set_chord_pitches_equal: bool = False,
) -> bool:
    assert isinstance(numbers, int | list | abjad.StaffPosition), repr(numbers)
    if isinstance(numbers, list):
        assert all(isinstance(_, int | abjad.StaffPosition) for _ in numbers)
    mutated_score = _do_staff_position_command(
        argument,
        [numbers],
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repitch=allow_repitch,
        mock=mock,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )
    return mutated_score


_staff_position_command = staff_position


def staff_positions(
    numbers,
    selector: typing.Callable = lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    mock: bool = False,
    exact: bool = False,
) -> StaffPositionCommand:
    return StaffPositionCommand(
        numbers=numbers,
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        exact=exact,
        mock=mock,
        selector=selector,
    )


def staff_positions_function(
    argument,
    numbers,
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repeats: bool = False,
    mock: bool = False,
    exact: bool = False,
) -> None:
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    mutated_score = _do_staff_position_command(
        argument,
        numbers,
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        # allow_repitch=allow_repitch,
        mock=mock,
        # set_chord_pitches_equal=set_chord_pitches_equal,
    )
    return mutated_score
