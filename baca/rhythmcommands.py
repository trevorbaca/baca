"""
Rhythm commands.
"""
import dataclasses
import types
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import command as _command
from . import select as _select
from . import sequence as _sequence
from . import tags as _tags
from .enums import enums as _enums


@dataclasses.dataclass
class RhythmCommand(_command.Command):

    rhythm_maker: typing.Any = None
    annotation_spanner_color: typing.Any = None
    annotation_spanner_text: typing.Any = None
    attach_not_yet_pitched: typing.Any = None
    frame: typing.Any = None
    match: typing.Any = None
    measures: typing.Any = None
    scope: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.annotation_spanner_color is not None:
            assert isinstance(self.annotation_spanner_color, str)
        if self.annotation_spanner_text is not None:
            assert isinstance(self.annotation_spanner_text, str)
        if self.attach_not_yet_pitched is not None:
            self.attach_not_yet_pitched = bool(self.attach_not_yet_pitched)
        self._check_rhythm_maker_input(self.rhythm_maker)

    def _check_rhythm_maker_input(self, rhythm_maker):
        if rhythm_maker is None:
            return
        prototype = (
            list,
            rmakers.RhythmMaker,
            rmakers.Assignment,
            rmakers.Stack,
            rmakers.Bind,
            typing.Callable,
        )
        if isinstance(rhythm_maker, prototype):
            return
        message = '\n  Input parameter "rhythm_maker" accepts:'
        message += "\n    rhythm-maker"
        message += "\n    selection"
        message += "\n    sequence of division assignment objects"
        message += "\n    none"
        message += '\n  Input parameter "rhythm_maker" received:'
        message += f"\n    {rhythm_maker!r}"
        raise Exception(message)

    def _make_components(
        self,
        time_signatures,
        runtime=None,
    ):
        rhythm_maker = self.rhythm_maker
        if isinstance(rhythm_maker, list):
            selection = rhythm_maker
            total_duration = sum([_.duration for _ in time_signatures])
            selection_duration = abjad.get.duration(selection)
            if selection_duration != total_duration:
                message = f"selection duration ({selection_duration}) does not"
                message += f" equal total duration ({total_duration})."
                raise Exception(message)
        else:
            if isinstance(self.rhythm_maker, rmakers.Stack):
                rcommand = self.rhythm_maker
            elif isinstance(self.rhythm_maker, types.FunctionType):
                rcommand = self.rhythm_maker
            else:
                rcommand = rmakers.stack(self.rhythm_maker)
            if isinstance(rcommand, rmakers.Stack):
                selection = rcommand(time_signatures)
            elif isinstance(rcommand, types.FunctionType):
                selection = rcommand(time_signatures)
        assert isinstance(selection, list), repr(selection)
        if self.attach_not_yet_pitched or not isinstance(self.rhythm_maker, list):
            container = abjad.Container(selection, name="Dummy")
            rest_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
            for leaf in abjad.iterate.leaves(container):
                if isinstance(leaf, abjad.Note | abjad.Chord):
                    abjad.attach(_enums.NOT_YET_PITCHED, leaf, tag=abjad.Tag())
                elif isinstance(leaf, rest_prototype):
                    pass
                else:
                    raise TypeError(leaf)
            container[:] = []
        return selection


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


def get_previous_section_stop_state(previous_section_voice_metadata, persist):
    previous_section_stop_state = None
    if previous_section_voice_metadata:
        previous_section_stop_state = previous_section_voice_metadata.get(
            _enums.RHYTHM.name
        )
        if (
            previous_section_stop_state is not None
            and previous_section_stop_state.get("name") != persist
        ):
            previous_section_stop_state = None
    return previous_section_stop_state


def make_even_divisions(time_signatures):
    rhythm_maker = rmakers.stack(
        rmakers.even_division([8]),
        rmakers.beam(),
        rmakers.extract_trivial(),
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 4)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> music = baca.make_monads("2/5 2/5 1/5")
        >>> score["Music"].extend(music)
        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
    maker = abjad.LeafMaker()
    pitch = 0
    for fraction in fractions.split():
        leaves = maker([pitch], [fraction])
        components.extend(leaves)
    for tuplet in abjad.select.tuplets(components):
        tuplet.multiplier = abjad.Multiplier(tuplet.multiplier)
    return components


def make_notes(
    time_signatures,
    *specifiers,
    repeat_ties: bool = False,
):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    if repeat_ties is True:
        repeat_tie_specifier = [rmakers.force_repeat_tie()]
    else:
        repeat_tie_specifier = []
    rhythm_maker = rmakers.stack(
        rmakers.note(),
        *specifiers,
        rmakers.rewrite_meter(),
        *repeat_tie_specifier,
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def make_repeat_tied_notes(
    time_signatures,
    *specifiers,
    do_not_rewrite_meter=None,
):
    r"""
    Makes repeat-tied notes; rewrites meter.

    ..  container:: example

        REGRESSION. All notes below are tagged NOT_YET_PITCHED_COLORING (and colored
        gold), even tied notes resulting from meter rewriting:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(10, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_repeat_tied_notes(commands.get())
        >>> score["Music"].extend(music)

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    specifiers_ = list(specifiers)
    specifier = rmakers.beam(lambda _: _select.plts(_))
    specifiers_.append(specifier)
    specifier = rmakers.repeat_tie(lambda _: _select.pheads(_)[1:])
    specifiers_.append(specifier)
    if not do_not_rewrite_meter:
        command = rmakers.rewrite_meter()
        specifiers_.append(command)
    specifier = rmakers.force_repeat_tie()
    specifiers_.append(specifier)
    rhythm_maker = rmakers.stack(
        rmakers.note(),
        *specifiers_,
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def make_repeated_duration_notes(
    time_signatures,
    durations,
    *specifiers,
    do_not_rewrite_meter=None,
):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]

    def preprocessor(divisions):
        divisions = _sequence.fuse(divisions)
        divisions = _sequence.split_divisions(divisions, durations, cyclic=True)
        return divisions

    rewrite_specifiers = []
    if not do_not_rewrite_meter:
        rewrite_specifiers.append(rmakers.rewrite_meter())
    rhythm_maker = rmakers.stack(
        rmakers.note(),
        *specifiers,
        *rewrite_specifiers,
        rmakers.force_repeat_tie(),
        preprocessor=preprocessor,
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def make_rests(time_signatures):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    rhythm_maker = rmakers.stack(
        rmakers.note(),
        rmakers.force_rest(lambda _: _select.lts(_)),
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def make_single_attack(time_signatures, duration):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    rhythm_maker = rmakers.stack(
        rmakers.incised(
            fill_with_rests=True,
            outer_divisions_only=True,
            prefix_talea=[numerator],
            prefix_counts=[1],
            talea_denominator=denominator,
        ),
        rmakers.beam(),
        rmakers.extract_trivial(),
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
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
    rhythm_maker = rmakers.stack(
        rmakers.note(),
        rmakers.beam(lambda _: _select.plts(_)),
        rmakers.tie(lambda _: _select.ptails(_)[:-1]),
        rmakers.rewrite_meter(),
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def make_tied_repeated_durations(time_signatures, durations):
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    specifiers = []
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    tie_specifier = rmakers.repeat_tie(lambda _: _select.pheads(_)[1:])
    specifiers.append(tie_specifier)
    tie_specifier = rmakers.force_repeat_tie()
    specifiers.append(tie_specifier)

    def preprocessor(divisions):
        divisions = _sequence.fuse(divisions)
        divisions = _sequence.split_divisions(divisions, durations, cyclic=True)
        return divisions

    rhythm_maker = rmakers.stack(
        rmakers.note(),
        *specifiers,
        preprocessor=preprocessor,
        tag=_tags.function_name(_frame()),
    )
    music = rhythm_maker(time_signatures)
    return music


def rhythm(
    *arguments,
    frame=None,
    preprocessor=None,
    measures=None,
    tag=abjad.Tag(),
):
    assert isinstance(tag, abjad.Tag), repr(tag)
    argument = rmakers.stack(*arguments, preprocessor=preprocessor, tag=tag)
    return RhythmCommand(
        rhythm_maker=argument,
        attach_not_yet_pitched=True,
        frame=frame,
        measures=measures,
    )
