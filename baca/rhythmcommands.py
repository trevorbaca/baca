"""
Rhythm commands.
"""
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import select as _select
from . import sequence as _sequence
from . import tags as _tags
from .enums import enums as _enums


class TimeSignatureMaker:

    __slots__ = (
        "_count",
        "_fermata_measures",
        "_rotation",
        "_time_signatures",
    )

    def __init__(
        self,
        time_signatures,
        *,
        count=None,
        fermata_measures=None,
        rotation=None,
    ):
        self._time_signatures = time_signatures
        if count is not None:
            assert isinstance(count, int), repr(count)
        self._count = count
        if fermata_measures is not None:
            assert all(isinstance(_, int) for _ in fermata_measures)
            fermata_measures = list(fermata_measures)
        self._fermata_measures = fermata_measures
        self._rotation = rotation

    def _normalize_fermata_measures(self):
        fermata_measures = []
        if self.fermata_measures is None:
            return fermata_measures
        for n in self.fermata_measures:
            if 0 < n:
                fermata_measures.append(n)
            elif n == 0:
                raise ValueError(n)
            else:
                fermata_measures.append(self.count - abs(n) + 1)
        fermata_measures.sort()
        return fermata_measures

    @property
    def count(self):
        """
        Gets count.
        """
        return self._count

    @property
    def fermata_measures(self):
        """
        Gets fermata measures.
        """
        return self._fermata_measures

    @property
    def rotation(self):
        """
        Gets rotation.
        """
        return self._rotation

    @property
    def time_signatures(self):
        """
        Gets time signatures.
        """
        return self._time_signatures

    def run(self):
        """
        Makes time signatures.

        Accounts for fermata measures.

        Does not account for stages.
        """
        if not self.count:
            raise Exception("must specify count with run().")
        result = []
        time_signatures = abjad.sequence.rotate(self.time_signatures, self.rotation)
        time_signatures = abjad.sequence.flatten(time_signatures, depth=1)
        time_signatures_ = abjad.CyclicTuple(time_signatures)
        i = 0
        fermata_measures = self._normalize_fermata_measures()
        for j in range(self.count):
            measure_number = j + 1
            if measure_number in fermata_measures:
                result.append(abjad.TimeSignature((1, 4)))
            else:
                time_signature = time_signatures_[i]
                result.append(time_signature)
                i += 1
        return result


def get_previous_rhythm_state(
    previous_parameter_to_state: dict, name: str
) -> dict | None:
    previous_rhythm_state = None
    if previous_parameter_to_state:
        previous_rhythm_state = previous_parameter_to_state.get(_enums.RHYTHM.name)
        if (
            previous_rhythm_state is not None
            and previous_rhythm_state.get("name") != name
        ):
            previous_rhythm_state = None
    if previous_rhythm_state is not None:
        assert len(previous_rhythm_state) in (4, 5), repr(previous_rhythm_state)
        assert previous_rhythm_state["name"] == name, repr(previous_rhythm_state)
    return previous_rhythm_state


def make_even_divisions(time_signatures):
    tag = _tags.function_name(_frame())
    nested_music = rmakers.even_division(time_signatures, [8], tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    rmakers.beam(voice, tag=tag)
    rmakers.extract_trivial(voice)
    music = abjad.mutate.eject_contents(voice)
    return music


def make_mmrests(time_signatures, *, head: str = ""):
    assert isinstance(head, str), repr(head)
    mmrests: list[abjad.MultimeasureRest | abjad.Container] = []
    if not head:
        tag = _tags.function_name(_frame(), n=1)
        for time_signature in time_signatures:
            multiplier = abjad.NonreducedFraction(time_signature.pair)
            mmrest = abjad.MultimeasureRest(1, multiplier=multiplier, tag=tag)
            mmrests.append(mmrest)
    else:
        assert isinstance(head, str)
        voice_name = head
        for i, time_signature in enumerate(time_signatures):
            multiplier = abjad.NonreducedFraction(time_signature.pair)
            if i == 0:
                tag = _tags.function_name(_frame(), n=2)
                tag = tag.append(_tags.HIDDEN)
                note_or_rest = _tags.NOTE
                tag = tag.append(_tags.NOTE)
                note = abjad.Note("c'1", multiplier=multiplier, tag=tag)
                abjad.override(note).Accidental.stencil = False
                abjad.override(note).NoteColumn.ignore_collision = True
                abjad.attach(_enums.NOTE, note)
                abjad.attach(_enums.NOT_YET_PITCHED, note)
                abjad.attach(_enums.HIDDEN, note)
                tag = _tags.function_name(_frame(), n=3)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music-coloring", site="before"
                )
                abjad.attach(literal, note, tag=tag)
                tag = _tags.function_name(_frame(), n=4)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music", site="before"
                )
                abjad.attach(literal, note, deactivate=True, tag=tag)
                # TODO: remove 1 line below?
                abjad.attach(_enums.HIDDEN, note)
                tag = _tags.function_name(_frame(), n=5)
                hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, hidden_note_voice)
                tag = _tags.function_name(_frame(), n=6)
                tag = tag.append(_tags.REST_VOICE)
                tag = tag.append(_tags.MULTIMEASURE_REST)
                rest = abjad.MultimeasureRest(1, multiplier=multiplier, tag=tag)
                abjad.attach(_enums.MULTIMEASURE_REST, rest)
                abjad.attach(_enums.REST_VOICE, rest)
                if "Music" in voice_name:
                    name = voice_name.replace("Music", "Rests")
                else:
                    assert "Voice" in voice_name
                    name = f"{voice_name}.Rests"
                tag = _tags.function_name(_frame(), n=7)
                multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, multimeasure_rest_voice)
                tag = _tags.function_name(_frame(), n=8)
                container = abjad.Container(
                    [hidden_note_voice, multimeasure_rest_voice],
                    simultaneous=True,
                    tag=tag,
                )
                abjad.attach(_enums.MULTIMEASURE_REST_CONTAINER, container)
                mmrests.append(container)
            else:
                mmrest = abjad.MultimeasureRest(1, multiplier=multiplier, tag=tag)
                mmrests.append(mmrest)
    return mmrests


def make_monads(fractions):
    r"""
    Makes monads.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> measures = baca.section.measures([(4, 4)])
        >>> baca.section.set_up_score(score, measures(), docs=True)
        >>> baca.SpacingSpecifier((1, 12))(score)
        >>> music = baca.make_monads("2/5 2/5 1/5")
        >>> score["Music"].extend(music)
        >>> _, _ = baca.section.postprocess_score(
        ...     score,
        ...     measures(),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/4
                        s1 * 4/4
                    }
                    \context Voice = "Music"
                    {
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            \baca-repeat-pitch-class-coloring
                            c'2
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            \baca-repeat-pitch-class-coloring
                            c'2
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            \baca-repeat-pitch-class-coloring
                            c'4
                        }
                    }
                >>
            }

    """
    components = []
    pitch = 0
    for fraction in fractions.split():
        leaves = abjad.makers.make_leaves([pitch], [fraction])
        components.extend(leaves)
    for tuplet in abjad.select.tuplets(components):
        tuplet.multiplier = abjad.Multiplier(tuplet.multiplier)
    return components


def make_notes(
    time_signatures,
    *,
    repeat_ties: bool = False,
):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    nested_music = rmakers.note(time_signatures, tag=tag)
    music = abjad.sequence.flatten(nested_music, depth=-1)
    music_voice = rmakers.wrap_in_time_signature_staff(music, time_signatures)
    rmakers.rewrite_meter(music_voice)
    if repeat_ties is True:
        rmakers.force_repeat_tie(music_voice)
    music = abjad.mutate.eject_contents(music_voice)
    return music


def make_repeat_tied_notes(
    time_signatures,
    *,
    do_not_rewrite_meter: bool = False,
) -> list[abjad.Leaf | abjad.Tuplet]:
    r"""
    Makes repeat-tied notes; rewrites meter.

    ..  container:: example

        REGRESSION. All notes below are tagged NOT_YET_PITCHED_COLORING (and colored
        gold), even tied notes resulting from meter rewriting:

        >>> score = baca.docs.make_empty_score(1)
        >>> measures = baca.section.measures([(10, 8)])
        >>> baca.section.set_up_score(score, measures(), docs=True)
        >>> baca.SpacingSpecifier((1, 12))(score)
        >>> music = baca.make_repeat_tied_notes(measures())
        >>> score["Music"].extend(music)

        >>> _, _ = baca.section.postprocess_score(
        ...     score,
        ...     measures(),
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
                        \baca-new-spacing-section #1 #12
                        \time 10/8
                        s1 * 10/8
                    }
                    \context Voice = "Music"
                    {
                        c'4.
                        - \tweak stencil ##f
                        ~
                        c'4
                        - \tweak stencil ##f
                        ~
                        \repeatTie
                        c'4.
                        - \tweak stencil ##f
                        ~
                        \repeatTie
                        c'4
                        \repeatTie
                    }
                >>
            }

    """
    tag = _tags.function_name(_frame())
    nested_music = rmakers.note(time_signatures, tag=tag)
    music: list[abjad.Leaf | abjad.Tuplet] = abjad.sequence.flatten(
        nested_music, depth=-1
    )
    music_voice = rmakers.wrap_in_time_signature_staff(music, time_signatures)
    rmakers.beam(_select.plts(music_voice))
    rmakers.repeat_tie(_select.pheads(music_voice)[1:], tag=tag)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(music_voice)
    rmakers.force_repeat_tie(music_voice)
    music = music_voice[:]
    music_voice[:] = []
    assert all(isinstance(_, abjad.Leaf | abjad.Tuplet) for _ in music)
    return music


def make_repeated_duration_notes(
    time_signatures,
    durations,
    *,
    do_not_rewrite_meter=None,
):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]

    def preprocessor(divisions):
        divisions = _sequence.fuse(divisions)
        divisions = _sequence.split_divisions(divisions, durations, cyclic=True)
        divisions = abjad.sequence.flatten(divisions, depth=-1)
        return divisions

    divisions = [abjad.NonreducedFraction(_) for _ in time_signatures]
    divisions = preprocessor(divisions)
    nested_music = rmakers.note(divisions, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(voice, tag=tag)
    rmakers.force_repeat_tie(voice)
    music = abjad.mutate.eject_contents(voice)
    return music


def make_rests(time_signatures):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    nested_music = rmakers.note(time_signatures, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    lts = _select.lts(voice)
    rmakers.force_rest(lts, tag=tag)
    music = abjad.mutate.eject_contents(voice)
    return music


def make_single_attack(time_signatures, duration):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    nested_music = rmakers.incised(
        time_signatures,
        fill_with_rests=True,
        outer_divisions_only=True,
        prefix_talea=[numerator],
        prefix_counts=[1],
        talea_denominator=denominator,
        tag=tag,
    )
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    rmakers.beam(voice)
    rmakers.extract_trivial(voice)
    music = abjad.mutate.eject_contents(voice)
    return music


def make_skeleton(
    argument: str | list,
    *,
    tag: abjad.Tag = abjad.Tag(),
):
    tag = _tags.function_name(_frame())
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate.eject_contents(container)
    elif isinstance(argument, list):
        selection = argument
    else:
        message = "baca.make_skeleton() accepts string or selection,"
        message += " not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        assert isinstance(tag, abjad.Tag), repr(tag)
        # TODO: tag attachments
        for component in abjad.iterate.components(selection):
            # TODO: do not set private attribute
            component._tag = tag
    return selection


def make_tied_notes(time_signatures):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    nested_music = rmakers.note(time_signatures, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    plts = _select.plts(voice)
    rmakers.beam(plts, tag=tag)
    ptails = _select.ptails(voice)[:-1]
    rmakers.tie(ptails, tag=tag)
    rmakers.rewrite_meter(voice, tag=tag)
    music = abjad.mutate.eject_contents(voice)
    return music


def make_tied_repeated_durations(time_signatures, durations):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    divisions = [abjad.NonreducedFraction(_) for _ in time_signatures]
    divisions = _sequence.fuse(divisions)
    divisions = _sequence.split_divisions(divisions, durations, cyclic=True)
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    nested_music = rmakers.note(divisions, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    pheads = _select.pheads(voice)[1:]
    rmakers.repeat_tie(pheads, tag=tag)
    rmakers.force_repeat_tie(voice)
    music = abjad.mutate.eject_contents(voice)
    return music
