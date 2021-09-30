"""
Rhythm commands.
"""
import inspect
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import const as _const
from . import overrides as _overrides
from . import scoping as _scoping
from . import selection as _selection
from . import sequence as _sequence
from . import tags as _tags


class RhythmCommand(_scoping.Command):
    r"""
    Rhythm command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ... )

        >>> command = baca.rhythm(
        ...     rmakers.even_division([8]),
        ...     rmakers.beam(),
        ...     rmakers.extract_trivial(),
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     command,
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     includes=["baca.ily"],
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     score=score,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 4/8
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'8
                        [
                        b'8
                        b'8
                        ]
                        b'8
                        [
                        b'8
                        b'8
                        b'8
                        ]
                        b'8
                        [
                        b'8
                        b'8
                        ]
                        b'8
                        [
                        b'8
                        b'8
                        b'8
                        ]
                    }
                >>
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_annotation_spanner_color",
        "_annotation_spanner_text",
        "_attach_not_yet_pitched",
        "_do_not_check_total_duration",
        "_frame",
        "_persist",
        "_rhythm_maker",
        "_state",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        rhythm_maker,
        *,
        annotation_spanner_color=None,
        annotation_spanner_text=None,
        attach_not_yet_pitched=None,
        do_not_check_total_duration=None,
        frame=None,
        match=None,
        measures=None,
        persist=None,
        scope=None,
    ):
        _scoping.Command.__init__(self, match=match, measures=measures, scope=scope)
        if annotation_spanner_color is not None:
            assert isinstance(annotation_spanner_color, str)
        self._annotation_spanner_color = annotation_spanner_color
        if annotation_spanner_text is not None:
            assert isinstance(annotation_spanner_text, str)
        self._annotation_spanner_text = annotation_spanner_text
        if attach_not_yet_pitched is not None:
            attach_not_yet_pitched = bool(attach_not_yet_pitched)
        self._attach_not_yet_pitched = attach_not_yet_pitched
        if do_not_check_total_duration is not None:
            do_not_check_total_duration = bool(do_not_check_total_duration)
        self._do_not_check_total_duration = do_not_check_total_duration
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        self._check_rhythm_maker_input(rhythm_maker)
        self._frame = frame
        self._rhythm_maker = rhythm_maker
        self._state = None

    ### PRIVATE METHODS ###

    def _check_rhythm_maker_input(self, rhythm_maker):
        if rhythm_maker is None:
            return
        prototype = (
            abjad.Selection,
            rmakers.RhythmMaker,
            rmakers.Assignment,
            rmakers.Stack,
            rmakers.Bind,
        )
        if isinstance(rhythm_maker, prototype):
            return
        message = '\n  Input parameter "rhythm_maker" accepts:'
        message += "\n    rhythm-maker"
        message += "\n    selection"
        message += "\n    sequence of division assignment objects"
        message += "\n    none"
        message += '\n  Input parameter "rhythm_maker" received:'
        message += f"\n    {abjad.storage(rhythm_maker)}"
        raise Exception(message)

    def _make_rhythm_annotation_string(self):
        if not self.frame:
            return
        frame_info = inspect.getframeinfo(self.frame)
        function_name = frame_info.function
        wrapped_arguments = abjad.Expression._wrap_arguments(self.frame)
        string = f"{function_name}({wrapped_arguments}) =|"
        return string

    def _make_selection(
        self,
        time_signatures,
        runtime=None,
    ):
        """
        Calls ``RhythmCommand`` on ``time_signatures``.
        """
        rhythm_maker = self.rhythm_maker
        if isinstance(rhythm_maker, abjad.Selection):
            selection = rhythm_maker
            total_duration = sum([_.duration for _ in time_signatures])
            selection_duration = abjad.get.duration(selection)
            if (
                not self.do_not_check_total_duration
                and selection_duration != total_duration
            ):
                message = f"selection duration ({selection_duration}) does not"
                message += f" equal total duration ({total_duration})."
                raise Exception(message)
        else:
            if isinstance(self.rhythm_maker, rmakers.Stack):
                rcommand = self.rhythm_maker
            else:
                rcommand = rmakers.stack(self.rhythm_maker)
            previous_segment_stop_state = self._previous_segment_stop_state(runtime)
            if isinstance(rcommand, rmakers.Stack):
                selection = rcommand(
                    time_signatures, previous_state=previous_segment_stop_state
                )
                self._state = rcommand.maker.state
            else:
                selection = rcommand(
                    time_signatures,
                    previous_segment_stop_state=previous_segment_stop_state,
                )
                self._state = rcommand.state
        assert isinstance(selection, abjad.Selection), repr(selection)
        if self.attach_not_yet_pitched or not isinstance(
            self.rhythm_maker, abjad.Selection
        ):
            container = abjad.Container(selection, name="Dummy")
            rest_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
            for leaf in abjad.iterate.leaves(container):
                if isinstance(leaf, (abjad.Note, abjad.Chord)):
                    abjad.attach(_const.NOT_YET_PITCHED, leaf, tag=None)
                elif isinstance(leaf, rest_prototype):
                    pass
                else:
                    raise TypeError(leaf)
            container[:] = []
        return selection

    def _previous_segment_stop_state(self, runtime):
        previous_segment_stop_state = None
        dictionary = runtime.get("previous_segment_voice_metadata")
        if dictionary:
            previous_segment_stop_state = dictionary.get(_const.RHYTHM)
            if (
                previous_segment_stop_state is not None
                and previous_segment_stop_state.get("name") != self.persist
            ):
                previous_segment_stop_state = None
        return previous_segment_stop_state

    ### PUBLIC PROPERTIES ###

    @property
    def annotation_spanner_color(self):
        """
        Gets annotation spanner color.
        """
        return self._annotation_spanner_color

    @property
    def annotation_spanner_text(self):
        """
        Gets annotation spanner text.
        """
        return self._annotation_spanner_text

    @property
    def attach_not_yet_pitched(self):
        """
        Is true when command attaches NOT_YET_PITCHED indicator.
        """
        return self._attach_not_yet_pitched

    @property
    def do_not_check_total_duration(self):
        """
        Is true when command does not check total duration.
        """
        return self._do_not_check_total_duration

    @property
    def frame(self):
        """
        Gets frame in which rhythm command was called.
        """
        return self._frame

    @property
    def parameter(self):
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.RhythmCommand(rmakers.note()).parameter
            'RHYTHM'

        """
        return _const.RHYTHM

    @property
    def persist(self):
        """
        Gets persist name.
        """
        return self._persist

    @property
    def rhythm_maker(self):
        r"""
        Gets selection, rhythm-maker or division assignment.

        ..  container:: example

            Talea rhythm-maker remembers previous state across gaps:

            >>> score = baca.docs.make_empty_score(1)
            >>> commands = baca.CommandAccumulator(
            ...     time_signatures=5 * [(4, 8)],
            ... )

            >>> note_command = rmakers.stack(
            ...     rmakers.note(),
            ...     rmakers.force_rest(
            ...         baca.selectors.lts(),
            ...     ),
            ...     rmakers.beam(baca.selectors.plts()),
            ... )
            >>> talea_command = rmakers.stack(
            ...     rmakers.talea([3, 4], 16),
            ...     rmakers.beam(),
            ...     rmakers.extract_trivial(),
            ... )
            >>> command = baca.rhythm(
            ...     rmakers.bind(
            ...         rmakers.assign(note_command, abjad.index([2])),
            ...         rmakers.assign(
            ...             talea_command,
            ...             abjad.index([0], 1),
            ...             remember_state_across_gaps=True,
            ...         ),
            ...     ),
            ... )

            >>> def label_with_durations(music):
            ...     return abjad.label.with_durations(
            ...         music,
            ...         direction=abjad.Down,
            ...         denominator=16,
            ...     )
            >>> commands(
            ...     "Music_Voice",
            ...     baca.label(label_with_durations),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
            ... )

            >>> lilypond_file = baca.interpret_commands(
            ...     commands.commands,
            ...     commands.time_signatures,
            ...     commands.voice_metadata,
            ...     includes=["baca.ily"],
            ...     move_global_context=True,
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ...     score=score,
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Music_Staff"
                    <<
                        \context Voice = "Global_Skips"
                        {
                            \baca-new-spacing-section #1 #16
                            \time 4/8
                            s1 * 1/2
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                            \baca-new-spacing-section #1 #4
                            s1 * 1/2
                        }
                        \context Voice = "Music_Voice"
                        {
                            \override TextScript.font-size = -2
                            \override TextScript.staff-padding = 5
                            b'8.
                            _ \markup {
                                \fraction
                                    3
                                    16
                                }
                            b'4
                            _ \markup {
                                \fraction
                                    4
                                    16
                                }
                            b'16
                            _ \markup {
                                \fraction
                                    3
                                    16
                                }
                            ~
                            b'8
                            b'4
                            _ \markup {
                                \fraction
                                    4
                                    16
                                }
                            b'8
                            _ \markup {
                                \fraction
                                    2
                                    16
                                }
                            r2
                            _ \markup {
                                \fraction
                                    8
                                    16
                                }
                            b'16
                            _ \markup {
                                \fraction
                                    1
                                    16
                                }
                            b'4
                            _ \markup {
                                \fraction
                                    4
                                    16
                                }
                            b'8.
                            _ \markup {
                                \fraction
                                    3
                                    16
                                }
                            b'4
                            _ \markup {
                                \fraction
                                    4
                                    16
                                }
                            b'8.
                            _ \markup {
                                \fraction
                                    3
                                    16
                                }
                            [
                            b'16
                            _ \markup {
                                \fraction
                                    1
                                    16
                                }
                            ]
                            \revert TextScript.font-size
                            \revert TextScript.staff-padding
                        }
                    >>
                }

        """
        return self._rhythm_maker

    @property
    def state(self):
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state


class TimeSignatureMaker:
    """
    Time-signature-maker.

    ..  container:: example

        >>> time_signatures = [
        ...     [(1, 16), (2, 16), (3, 16)],
        ...     [(1, 8), (2, 8), (3, 8)],
        ... ]
        >>> maker = baca.TimeSignatureMaker(
        ...     time_signatures=time_signatures,
        ...     count=5,
        ...     fermata_measures=[5],
        ... )
        >>> maker.run()
        [(1, 16), (2, 16), (3, 16), (1, 8), TimeSignature((1, 4))]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_count",
        "_fermata_measures",
        "_rotation",
        "_time_signatures",
    )

    ### INITIALIZER ###

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

    ### PRIVATE METHODS ###

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

    ### PUBLIC PROPERTIES ###

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

    ### PUBLIC METHODS ###

    def run(self):
        """
        Makes time signatures (without stages).

        Accounts for fermata measures.

        Does not account for stages.
        """
        if not self.count:
            raise Exception("must specify count with run().")
        result = []
        time_signatures = abjad.Sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
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


def make_even_divisions(*, measures=None):
    """
    Makes even divisions.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.even_division([8]),
            rmakers.beam(),
            rmakers.extract_trivial(),
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_fused_tuplet_monads(
    *,
    measures=None,
    tuplet_ratio=None,
):
    """
    Makes fused tuplet monads.
    """
    tuplet_ratios = []
    if tuplet_ratio is None:
        tuplet_ratios.append((1,))
    else:
        tuplet_ratios.append(tuplet_ratio)
    return RhythmCommand(
        rmakers.stack(
            rmakers.tuplet(tuplet_ratios),
            rmakers.beam(),
            rmakers.rewrite_rest_filled(),
            rmakers.trivialize(),
            rmakers.extract_trivial(),
            rmakers.force_repeat_tie(),
            preprocessor=lambda _: _sequence.Sequence([_sequence.Sequence(_).sum()]),
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_monads(fractions):
    r"""
    Makes monads.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 4)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_monads("2/5 2/5 1/5"),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     includes=["baca.ily"],
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     score=score,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #4
                        \time 4/4
                        s1 * 1
                    }
                    \context Voice = "Music_Voice"
                    {
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            b'2
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            b'2
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/5
                        {
                            b'4
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
    for tuplet in abjad.select(components).tuplets():
        tuplet.multiplier = abjad.Multiplier(tuplet.multiplier)
    rhythm_maker = abjad.select(components)
    return RhythmCommand(
        rhythm_maker,
        annotation_spanner_color="#darkcyan",
        attach_not_yet_pitched=True,
        frame=_frame(),
    )


def make_notes(
    *specifiers,
    measures=None,
    repeat_ties=False,
):
    """
    Makes notes; rewrites meter.
    """
    if repeat_ties:
        repeat_tie_specifier = [rmakers.force_repeat_tie()]
    else:
        repeat_tie_specifier = []
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            rmakers.rewrite_meter(),
            *repeat_tie_specifier,
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_repeat_tied_notes(
    *specifiers,
    do_not_rewrite_meter=None,
    measures=None,
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

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_repeat_tied_notes(),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     includes=["baca.ily"],
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     score=score,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #4
                        \time 10/8
                        s1 * 5/4
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak stencil ##f
                        ~
                        b'4
                        \repeatTie
                        - \tweak stencil ##f
                        ~
                        b'4.
                        \repeatTie
                        - \tweak stencil ##f
                        ~
                        b'4
                        \repeatTie
                    }
                >>
            }

    """
    specifiers_ = list(specifiers)
    specifier = rmakers.beam(lambda _: _selection.Selection(_).plts())
    specifiers_.append(specifier)
    specifier = rmakers.repeat_tie(lambda _: _selection.Selection(_).pheads()[1:])
    specifiers_.append(specifier)
    if not do_not_rewrite_meter:
        command = rmakers.rewrite_meter()
        specifiers_.append(command)
    specifier = rmakers.force_repeat_tie()
    specifiers_.append(specifier)
    return RhythmCommand(
        rmakers.stack(rmakers.note(), *specifiers_, tag=_scoping.site(_frame())),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
    )


def make_repeated_duration_notes(
    durations,
    *specifiers,
    do_not_rewrite_meter=None,
    measures=None,
):
    """
    Makes repeated-duration notes; rewrites meter.
    """
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]

    def preprocessor(divisions):
        divisions = _sequence.Sequence(divisions)
        divisions = divisions.fuse()
        divisions = divisions.split_divisions(durations, cyclic=True)
        return divisions

    rewrite_specifiers = []
    if not do_not_rewrite_meter:
        rewrite_specifiers.append(rmakers.rewrite_meter())
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            *rewrite_specifiers,
            rmakers.force_repeat_tie(),
            preprocessor=preprocessor,
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_rests(*, measures=None):
    """
    Makes rests.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.force_rest(lambda _: _selection.Selection(_).lts()),
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_single_attack(duration, *, measures=None):
    """
    Makes single attacks with ``duration``.
    """
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    return RhythmCommand(
        rmakers.stack(
            rmakers.incised(
                fill_with_rests=True,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
            ),
            rmakers.beam(),
            rmakers.extract_trivial(),
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_tied_notes(*, measures=None):
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.beam(lambda _: _selection.Selection(_).plts()),
            rmakers.tie(lambda _: _selection.Selection(_).ptails()[:-1]),
            rmakers.rewrite_meter(),
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def make_tied_repeated_durations(durations, *, measures=None):
    """
    Makes tied repeated durations; does not rewrite meter.
    """
    specifiers = []
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    tie_specifier = rmakers.repeat_tie(lambda _: _selection.Selection(_).pheads()[1:])
    specifiers.append(tie_specifier)
    tie_specifier = rmakers.force_repeat_tie()
    specifiers.append(tie_specifier)

    def preprocessor(divisions):
        divisions = _sequence.Sequence(divisions)
        divisions = divisions.fuse()
        divisions = divisions.split_divisions(durations, cyclic=True)
        return divisions

    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            preprocessor=preprocessor,
            tag=_scoping.site(_frame()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=_frame(),
        measures=measures,
    )


def music(
    argument,
    *,
    do_not_check_total_duration=None,
    tag=abjad.Tag("baca.music()"),
):
    """
    Makes rhythm command from string or selection ``argument``.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate.eject_contents(container)
    elif isinstance(argument, abjad.Selection):
        selection = argument
    else:
        message = "baca.music() accepts string or selection,"
        message += f" not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection,
        annotation_spanner_color="#darkcyan",
        annotation_spanner_text="baca.music() =|",
        do_not_check_total_duration=do_not_check_total_duration,
    )


def rhythm(
    *arguments,
    frame=None,
    preprocessor=None,
    measures=None,
    persist=None,
    tag=None,
):
    """
    Makes rhythm command from ``argument``.
    """
    if tag is not None:
        assert isinstance(tag, abjad.Tag), repr(tag)
    argument = rmakers.stack(*arguments, preprocessor=preprocessor, tag=tag)
    return RhythmCommand(
        argument,
        attach_not_yet_pitched=True,
        frame=frame,
        measures=measures,
        persist=persist,
    )


def skeleton(
    argument,
    *,
    do_not_check_total_duration=None,
    tag=abjad.Tag("baca.skeleton()"),
):
    """
    Makes rhythm command from ``string`` and attaches NOT_YET_PITCHED indicators to
    music.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate.eject_contents(container)
    elif isinstance(argument, abjad.Selection):
        selection = argument
    else:
        message = "baca.skeleton() accepts string or selection,"
        message += " not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection,
        annotation_spanner_color="#darkcyan",
        annotation_spanner_text="baca.skeleton() =|",
        attach_not_yet_pitched=True,
        do_not_check_total_duration=do_not_check_total_duration,
    )


def tacet(
    color="#green",
    *,
    measures=None,
    selector=lambda _: _selection.Selection(_).mmrests(),
):
    """
    Colors multimeasure rests.
    """
    command = _overrides.mmrest_color(color, selector=selector)
    _scoping.tag(_tags.TACET_COLORING, command)
    _scoping.tag(_scoping.site(_frame()), command)
    command_ = _scoping.new(command, measures=measures)
    assert isinstance(command_, _overrides.OverrideCommand)
    return command_


def tag_selection(selection, tag):
    """
    Tags selection.
    """
    assert isinstance(tag, abjad.Tag), repr(tag)
    # TODO: tag attachments
    for component in abjad.iterate.components(selection):
        component._tag = tag
